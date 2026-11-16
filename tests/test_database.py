"""Pruebas del pool de conexiones (app/core/database.py).

Regresion: `ThreadedConnectionPool.getconn()` no espera; si varias peticiones
llegan a la vez (el panel carga todos los modulos en paralelo) el pool se
agotaba y la API respondia 503 aunque la base de datos estuviera disponible.
"""

from __future__ import annotations

import threading

import pytest

from app.core import database as modulo_database
from app.core.database import Database


class _ConexionFalsa:
    """Conexion minima con commit/rollback, como la de psycopg2."""

    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


class _PoolFalso:
    """Pool simulado que solo admite `maximo` conexiones simultaneas."""

    def __init__(self, maximo: int = 2) -> None:
        self.maximo = maximo
        self.conexiones: list[_ConexionFalsa] = []
        self.devueltas = 0

    def getconn(self):
        if len(self.conexiones) >= self.maximo:
            raise AssertionError("el pool se agoto: deberia haber esperado turno")
        conexion = _ConexionFalsa()
        self.conexiones.append(conexion)
        return conexion

    def putconn(self, conexion) -> None:
        self.conexiones.remove(conexion)
        self.devueltas += 1


@pytest.fixture
def pool_pequeno(monkeypatch):
    """Pool de 2 conexiones, con un semaforo de 2 turnos."""
    pool = _PoolFalso(maximo=2)
    monkeypatch.setattr(Database, "_pool", pool)
    monkeypatch.setattr(Database, "_turnos", threading.Semaphore(2))
    monkeypatch.setattr(Database, "_lock", threading.Lock())
    return pool


def test_una_conexion_se_devuelve_al_pool_al_salir_del_bloque(pool_pequeno):
    db = Database()
    with db.get_connection():
        pass
    assert pool_pequeno.conexiones == []
    assert pool_pequeno.devueltas == 1


def test_las_peticiones_simultaneas_esperan_turno_en_lugar_de_fallar(pool_pequeno):
    """Varias peticiones a la vez no agotan el pool: esperan su turno."""
    db = Database()
    errores: list[Exception] = []
    barrera = threading.Barrier(4, timeout=5)

    def trabajar() -> None:
        try:
            barrera.wait()
            with db.get_connection():
                pass
        except Exception as exc:  # pragma: no cover - solo para el diagnostico
            errores.append(exc)

    hilos = [threading.Thread(target=trabajar) for _ in range(4)]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join(timeout=10)

    assert not errores, f"hubo errores por saturacion del pool: {errores}"
    assert pool_pequeno.conexiones == []


def test_una_conexion_con_error_se_devuelve_igualmente(pool_pequeno):
    """Si el bloque lanza error, la conexion vuelve al pool (con rollback)."""
    db = Database()
    with pytest.raises(ValueError):
        with db.get_connection():
            raise ValueError("fallo simulado")
    assert pool_pequeno.conexiones == []
    assert pool_pequeno.devueltas == 1


def test_el_semaphore_se_libera_al_devolver_la_conexion(pool_pequeno):
    """El semaforo de turnos queda libre despues de cada uso."""
    db = Database()
    turnos = Database._turnos
    assert turnos is not None
    assert turnos.acquire(blocking=False) is True  # hay 2 turnos
    assert turnos.acquire(blocking=False) is True
    turnos.release()
    turnos.release()
    with db.get_connection():
        pass
    # Tras el uso, los dos turnos vuelven a estar disponibles.
    assert turnos.acquire(blocking=False) is True
    assert turnos.acquire(blocking=False) is True
    turnos.release()
    turnos.release()


def test_el_503_por_pool_agotado_no_filtra_credenciales(monkeypatch):
    """Si se agota el pool, el mensaje no incluye la contrasena."""
    monkeypatch.setenv("DB_PASSWORD", "secreto123")
    error = modulo_database._error_503(
        modulo_database.MSG_POOL_AGOTADO, "prueba", None
    )
    assert error.status_code == 503
    assert "secreto123" not in str(error.detail)
