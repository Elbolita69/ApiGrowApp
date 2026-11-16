"""Pruebas del pool de conexiones (app/core/database.py).

Regresion: `psycopg2.pool.ThreadedConnectionPool.getconn()` no espera; si
varias peticiones llegan a la vez (el panel carga todos los modulos en
paralelo) el pool se agotaba y la API respondia 503 aunque la base de
datos estuviera disponible. El pool propio espera su turno y ademas abre
las conexiones en paralelo.
"""

from __future__ import annotations

import threading
import time

import pytest

import psycopg2

from app.core import database as modulo_database
from app.core.database import Database, _PoolDeConexiones


class _ConexionFalsa:
    """Conexion minima con commit/rollback, como la de psycopg2."""

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
    """Pool que fabrica conexiones falsas en vez de abrir conexiones reales."""

    def __init__(self, maximo: int = 2, timeout: int = 5) -> None:
        super().__init__(maximo, timeout)
        self.creadas = 0

    def _nueva_conexion(self) -> _ConexionFalsa:
        self.creadas += 1
        return _ConexionFalsa()


@pytest.fixture
def db_con_pool(monkeypatch):
    """Database con un pool de prueba inyectado."""
    pool = _PoolDePrueba(maximo=2, timeout=5)
    monkeypatch.setattr(Database, "_pool", pool)
    monkeypatch.setattr(Database, "_lock", threading.Lock())

    db = Database()
    db._abrir_conexion = lambda: pool._nueva_conexion()  # type: ignore[method-assign]
    return db


def test_una_conexion_se_devuelve_al_pool_al_salir_del_bloque(db_con_pool):
    with db_con_pool.get_connection():
        pass
    pool = Database._pool
    assert pool is not None
    assert len(pool._libres) == 1
    assert pool.creadas == 1


def test_las_peticiones_simultaneas_esperan_turno_en_lugar_de_fallar(db_con_pool):
    """Varias peticiones a la vez no agotan el pool: esperan su turno."""
    errores: list[Exception] = []
    barrera = threading.Barrier(4, timeout=5)

    def trabajar() -> None:
        try:
            barrera.wait()
            with db_con_pool.get_connection():
                pass
        except Exception as exc:  # pragma: no cover - solo diagnostico
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
    """Si el bloque lanza error, la conexion vuelve al pool (con rollback)."""
    with pytest.raises(ValueError):
        with db_con_pool.get_connection():
            raise ValueError("fallo simulado")
    pool = Database._pool
    assert pool is not None
    assert len(pool._libres) == 1


def test_la_espera_del_turno_termina_con_error_controlado():
    """Si no hay conexiones libres en el plazo, el error es controlado."""
    pool = _PoolDeConexiones(maximo=1, timeout=1)
    conexion, _ociosa, hay_que_crear = pool.reservar()
    assert hay_que_crear is True
    with pytest.raises(TimeoutError):
        pool.reservar()


def test_el_precalentamiento_abre_las_conexiones_en_paralelo(monkeypatch):
    """`precalentar` abre varias conexiones a la vez, no de una en una."""
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

    db._abrir_conexion = conexion_lenta  # type: ignore[method-assign]

    inicio = time.monotonic()
    db.precalentar()
    total = time.monotonic() - inicio
    tiempos.append(total)

    assert len(abiertas) == 6
    # En serie serian 6 x 0.3 s = 1.8 s; en paralelo deben ser mucho menos.
    assert total < demora * 3, f"las conexiones se abrieron en serie: {total:.2f}s"


def test_una_conexion_muerta_se_descarta_y_se_prueba_otra(db_con_pool):
    """Si el servidor cerro la conexion, se descarta y se abre otra.

    En Neon las conexiones inactivas se cierran y en Render las instancias
    se duermen: reciclar una conexion muerta devolvia 503 al usuario.
    """
    pool = Database._pool
    assert pool is not None
    muerta = _ConexionFalsa()
    # Se simula una conexion que el servidor ya cerro.
    def cursor_roto(*_args, **_kwargs):
        raise psycopg2.OperationalError("server closed the connection unexpectedly")
    muerta.cursor = cursor_roto  # type: ignore[method-assign]
    pool._libres.append((muerta, time.monotonic() - 999))

    db = db_con_pool
    db.conn_max_idle = 1  # cualquier conexion ociosa se valida
    conexion = db.get_connection()
    try:
        assert conexion._raw is not muerta
    finally:
        conexion.close()


def test_una_conexion_rota_al_cerrar_no_vuelve_al_pool(db_con_pool):
    """Si el commit falla, la conexion se descarta en vez de reciclarse."""
    class _ConexionRota(_ConexionFalsa):
        def commit(self):
            raise psycopg2.OperationalError("server closed the connection unexpectedly")

    db = db_con_pool
    rota = _ConexionRota()
    crudo = db._abrir_conexion()
    crudo.commit = rota.commit  # type: ignore[method-assign]
    crudo.rollback = lambda: None  # type: ignore[method-assign]

    from app.core.database import ConexionPool
    envoltura = ConexionPool(db, crudo)
    envoltura.close()

    pool = Database._pool
    assert pool is not None
    # No debe haber devuelto la conexion rota al pool.
    assert all(c is not crudo for c, _ in pool._libres)


def test_cerrar_el_pool_libera_las_conexiones(db_con_pool):
    with db_con_pool.get_connection():
        pass
    db_con_pool.close_pool()
    assert Database._pool is None


def test_el_503_por_pool_agotado_no_filtra_credenciales(monkeypatch):
    """Si se agota el pool, el mensaje no incluye la contrasena."""
    monkeypatch.setenv("DB_PASSWORD", "secreto123")
    error = modulo_database._error_503(
        modulo_database.MSG_POOL_AGOTADO, "prueba", None
    )
    assert error.status_code == 503
    assert "secreto123" not in str(error.detail)
