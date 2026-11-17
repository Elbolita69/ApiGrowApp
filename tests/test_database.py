from __future__ import annotations

import threading
import time

import pytest

import psycopg2

from app.core import database as modulo_database
from app.core.database import Database, _PoolDeConexiones


class _ConexionFalsa:
    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0
        self.cerrada = False

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def close(self) -> None:
        self.cerrada = True


class _PoolDePrueba(_PoolDeConexiones):
    def __init__(self, maximo: int = 2, timeout: int = 5) -> None:
        super().__init__(maximo, timeout)
        self.creadas = 0

    def _nueva_conexion(self) -> _ConexionFalsa:
        self.creadas += 1
        return _ConexionFalsa()


@pytest.fixture
def db_con_pool(monkeypatch):
    pool = _PoolDePrueba(maximo=2, timeout=5)
    monkeypatch.setattr(Database, "_pool", pool)
    monkeypatch.setattr(Database, "_lock", threading.Lock())

    db = Database()
    db._abrir_conexion = lambda: pool._nueva_conexion()
    return db


def test_una_conexion_se_devuelve_al_pool_al_salir_del_bloque(db_con_pool):
    with db_con_pool.get_connection():
        pass
    pool = Database._pool
    assert pool is not None
    assert len(pool._libres) == 1
    assert pool.creadas == 1


def test_las_peticiones_simultaneas_esperan_turno_en_lugar_de_fallar(db_con_pool):
    errores: list[Exception] = []
    barrera = threading.Barrier(4, timeout=5)

    def trabajar() -> None:
        try:
            barrera.wait()
            with db_con_pool.get_connection():
                pass
        except Exception as exc:
            errores.append(exc)

    hilos = [threading.Thread(target=trabajar) for _ in range(4)]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join(timeout=10)

    assert not errores, f"hubo errores por saturacion del pool: {errores}"
    pool = Database._pool
    assert pool is not None
    assert len(pool._libres) == pool.creadas


def test_una_conexion_con_error_se_devuelve_igualmente(db_con_pool):
    with pytest.raises(ValueError):
        with db_con_pool.get_connection():
            raise ValueError("fallo simulado")
    pool = Database._pool
    assert pool is not None
    assert len(pool._libres) == 1


def test_la_espera_del_turno_termina_con_error_controlado():
    pool = _PoolDeConexiones(maximo=1, timeout=1)
    conexion, _ociosa, hay_que_crear = pool.reservar()
    assert hay_que_crear is True
    with pytest.raises(TimeoutError):
        pool.reservar()


def test_el_precalentamiento_abre_las_conexiones_en_paralelo(monkeypatch):
    pool = _PoolDePrueba(maximo=6, timeout=5)
    monkeypatch.setattr(Database, "_pool", pool)
    db = Database()
    db.pool_min = 6
    db.pool_max = 6

    tiempos: list[float] = []
    demora = 0.3
    abiertas: list[_ConexionFalsa] = []

    def conexion_lenta():
        time.sleep(demora)
        conexion = _ConexionFalsa()
        abiertas.append(conexion)
        return conexion

    db._abrir_conexion = conexion_lenta

    inicio = time.monotonic()
    db.precalentar()
    total = time.monotonic() - inicio
    tiempos.append(total)

    assert len(abiertas) == 6
    assert total < demora * 3, f"las conexiones se abrieron en serie: {total:.2f}s"


def test_una_conexion_muerta_se_descarta_y_se_prueba_otra(db_con_pool):
    pool = Database._pool
    assert pool is not None
    muerta = _ConexionFalsa()
    def cursor_roto(*_args, **_kwargs):
        raise psycopg2.OperationalError("server closed the connection unexpectedly")
    muerta.cursor = cursor_roto
    pool._libres.append((muerta, time.monotonic() - 999))

    db = db_con_pool
    db.conn_max_idle = 1
    conexion = db.get_connection()
    try:
        assert conexion._raw is not muerta
    finally:
        conexion.close()


def test_una_conexion_rota_al_cerrar_no_vuelve_al_pool(db_con_pool):
    class _ConexionRota(_ConexionFalsa):
        def commit(self):
            raise psycopg2.OperationalError("server closed the connection unexpectedly")

    db = db_con_pool
    rota = _ConexionRota()
    crudo = db._abrir_conexion()
    crudo.commit = rota.commit
    crudo.rollback = lambda: None

    from app.core.database import ConexionPool
    envoltura = ConexionPool(db, crudo)
    envoltura.close()

    pool = Database._pool
    assert pool is not None
    assert all(c is not crudo for c, _ in pool._libres)


def test_cerrar_el_pool_libera_las_conexiones(db_con_pool):
    with db_con_pool.get_connection():
        pass
    db_con_pool.close_pool()
    assert Database._pool is None


def test_el_503_por_pool_agotado_no_filtra_credenciales(monkeypatch):
    monkeypatch.setenv("DB_PASSWORD", "secreto123")
    error = modulo_database._error_503(
        modulo_database.MSG_POOL_AGOTADO, "prueba", None
    )
    assert error.status_code == 503
    assert "secreto123" not in str(error.detail)
