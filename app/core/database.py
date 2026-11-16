"""Acceso a PostgreSQL con psycopg2 (driver sincrono).

Decisiones del taller:
- El driver es `psycopg2` (sincrono). Por eso los routers usan handlers
  sincronos (`def`): FastAPI los ejecuta en su threadpool y una conexion nunca
  se comparte entre hilos.
- Las conexiones se toman de un `ThreadedConnectionPool` y se devuelven al pool
  al salir del bloque `with`. Nunca se usa una conexion global.
- El borrado es logico (`estado = FALSE`); aqui no hay ninguna sentencia de
  borrado fisico.
"""

from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any, Optional, Sequence

import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException, status
from psycopg2 import pool as psycopg2_pool
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

# Raiz del proyecto: app/core/database.py -> app/core -> app -> <raiz>
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

MSG_SIN_CONEXION = (
    "No se pudo conectar con la base de datos en este momento. Intente de nuevo."
)
MSG_POOL_AGOTADO = (
    "No hay conexiones disponibles con la base de datos en este momento. Intente de nuevo."
)


def _sanear(texto: str) -> str:
    """Oculta la contrasena de la base de datos si aparece en un mensaje."""
    clave = os.getenv("DB_PASSWORD")
    if clave and clave in texto:
        return texto.replace(clave, "***")
    return texto


def _error_503(mensaje: str, contexto: str, exc: Optional[BaseException] = None) -> HTTPException:
    """Registra el error con contexto y devuelve un 503 en espanol (sin secretos)."""
    if exc is not None:
        logger.error(
            "Error de base de datos en %s: %s: %s",
            contexto,
            type(exc).__name__,
            _sanear(str(exc)),
        )
    else:
        logger.error("Error de base de datos en %s", contexto)
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=mensaje,
    )


class ConexionPool:
    """Conexion tomada del pool de psycopg2.

    Se usa como context manager:

        with db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT 1;")

    Al salir del bloque se hace commit (o rollback si hubo error) y la conexion
    vuelve al pool. `conn` dentro del bloque es la conexion cruda de psycopg2.
    """

    __slots__ = ("_db", "_raw", "_cerrada")

    def __init__(self, db: "Database", raw: Any) -> None:
        self._db = db
        self._raw = raw
        self._cerrada = False

    def __enter__(self) -> Any:
        return self._raw

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close(rollback=exc_type is not None)
        return False

    def close(self, rollback: bool = False) -> None:
        if self._cerrada:
            return
        self._cerrada = True
        raw = self._raw
        try:
            if rollback:
                raw.rollback()
            else:
                raw.commit()
        except psycopg2.Error as exc:
            logger.error("No se pudo cerrar la transaccion: %s", _sanear(str(exc)))
            try:
                raw.rollback()
            except psycopg2.Error:
                pass
        finally:
            self._db.release_connection(raw)

    def __getattr__(self, nombre: str) -> Any:
        # Delegacion transparente hacia la conexion cruda de psycopg2.
        if nombre.startswith("__") or nombre in ("_db", "_raw", "_cerrada"):
            raise AttributeError(nombre)
        return getattr(self._raw, nombre)


class Database:
    """Pool de conexiones a PostgreSQL (psycopg2, sincrono).

    Todas las instancias comparten un unico pool (importante en Neon, que
    limita el numero de conexiones simultaneas).

    `ThreadedConnectionPool.getconn()` NO espera: si no hay una conexion
    libre lanza `PoolError` de inmediato. Como el panel carga varios modulos
    en paralelo, eso agotaba el pool y devolvia 503. Por eso hay un
    semaforo: cada peticion toma un turno y espera a que haya conexion
    libre en lugar de fallar.
    """

    _pool: Optional[psycopg2_pool.ThreadedConnectionPool] = None
    _turnos: Optional[threading.Semaphore] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", "5432") or 5432)
        # DB_SSL=false para una base local; en la nube (Neon) se deja en true
        self.ssl = os.getenv("DB_SSL", "true").strip().lower() != "false"
        self.pool_min = max(1, int(os.getenv("DB_POOL_MIN", "1") or 1))
        self.pool_max = max(self.pool_min, int(os.getenv("DB_POOL_MAX", "5") or 5))
        # Espera maxima por una conexion libre (segundos).
        self.pool_timeout = max(1, int(os.getenv("DB_POOL_TIMEOUT", "20") or 20))

    # ------------------------------------------------------------------ pool
    def get_pool(self) -> psycopg2_pool.ThreadedConnectionPool:
        """Devuelve (creandolo si hace falta) el pool de conexiones."""
        if Database._pool is None:
            with Database._lock:
                if Database._pool is None:
                    Database._pool = self._crear_pool()
                    Database._turnos = threading.Semaphore(self.pool_max)
        return Database._pool

    def _crear_pool(self) -> psycopg2_pool.ThreadedConnectionPool:
        try:
            return psycopg2_pool.ThreadedConnectionPool(
                self.pool_min,
                self.pool_max,
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password,
                sslmode="require" if self.ssl else "disable",
                connect_timeout=10,
            )
        except psycopg2.Error as exc:
            raise _error_503(MSG_SIN_CONEXION, "creacion del pool", exc)

    def _tomar_turno(self) -> None:
        """Espera a que haya una conexion libre del pool.

        Sin esta espera, varias peticiones simultaneas agotan el pool y
        devuelven 503 aunque la base de datos este perfectamente disponible.
        """
        self.get_pool()
        turno = Database._turnos
        if turno is None:  # pragma: no cover - defensa ante poolManual
            return
        if not turno.acquire(timeout=self.pool_timeout):
            raise _error_503(MSG_POOL_AGOTADO, "espera de conexion libre", None)

    def _liberar_turno(self) -> None:
        turno = Database._turnos
        if turno is not None:
            turno.release()

    def get_connection(self) -> ConexionPool:
        """Toma una conexion del pool (usable como context manager)."""
        self._tomar_turno()
        pool_ = self.get_pool()
        try:
            raw = pool_.getconn()
        except psycopg2.Error as exc:
            self._liberar_turno()
            raise _error_503(MSG_POOL_AGOTADO, "obtencion de conexion", exc)
        return ConexionPool(self, raw)

    def release_connection(self, conn: Any) -> None:
        """Devuelve una conexion al pool."""
        raw = conn._raw if isinstance(conn, ConexionPool) else conn
        pool_ = Database._pool
        if pool_ is None:
            self._liberar_turno()
            return
        try:
            pool_.putconn(raw)
        except psycopg2.Error as exc:
            logger.error("No se pudo devolver la conexion al pool: %s", _sanear(str(exc)))
        finally:
            self._liberar_turno()

    def close_pool(self) -> None:
        """Cierra el pool y todas sus conexiones."""
        with Database._lock:
            if Database._pool is not None:
                try:
                    Database._pool.closeall()
                except psycopg2.Error as exc:
                    logger.error("No se pudo cerrar el pool: %s", _sanear(str(exc)))
                finally:
                    Database._pool = None
                    Database._turnos = None

    # --------------------------------------------------------------- helpers
    def consultar(self, sql: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
        """Ejecuta una consulta y devuelve las filas como lista de diccionarios."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return [dict(fila) for fila in cur.fetchall()]

    def consultar_uno(self, sql: str, params: Optional[Sequence[Any]] = None) -> Optional[dict]:
        """Ejecuta una consulta y devuelve la primera fila (o None)."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                fila = cur.fetchone()
                return dict(fila) if fila else None
