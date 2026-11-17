from __future__ import annotations

import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Optional, Sequence

import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException, status
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

MSG_SIN_CONEXION = (
    "No se pudo conectar con la base de datos en este momento. Intente de nuevo."
)
MSG_POOL_AGOTADO = (
    "No hay conexiones disponibles con la base de datos en este momento. Intente de nuevo."
)


def _sanear(texto: str) -> str:
    clave = os.getenv("DB_PASSWORD")
    if clave and clave in texto:
        return texto.replace(clave, "***")
    return texto


def _error_503(mensaje: str, contexto: str, exc: Optional[BaseException] = None) -> HTTPException:
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
            logger.warning("Conexion descartada al cerrarla: %s", _sanear(str(exc)))
            self._db.descartar_conexion(raw)
            return
        self._db.release_connection(raw)

    def __getattr__(self, nombre: str) -> Any:
        if nombre.startswith("__") or nombre in ("_db", "_raw", "_cerrada"):
            raise AttributeError(nombre)
        return getattr(self._raw, nombre)


class _PoolDeConexiones:
    def __init__(self, maximo: int, timeout: int) -> None:
        self.maximo = maximo
        self.timeout = timeout
        self._libres: list[tuple[Any, float]] = []
        self._creadas = 0
        self._cerrado = False
        self._cond = threading.Condition()

    def reservar(self) -> tuple[Optional[Any], float, bool]:
        with self._cond:
            if self._cerrado:
                raise RuntimeError("El pool de conexiones esta cerrado.")
            if self._libres:
                conexion, devuelta = self._libres.pop()
                return conexion, devuelta, False
            if self._creadas < self.maximo:
                self._creadas += 1
                return None, 0.0, True
            limite = time.monotonic() + self.timeout
            while True:
                restante = limite - time.monotonic()
                if restante <= 0:
                    raise TimeoutError("No hay conexiones libres del pool.")
                self._cond.wait(restante)
                if self._libres:
                    conexion, devuelta = self._libres.pop()
                    return conexion, devuelta, False

    def cancelar_reserva(self) -> None:
        with self._cond:
            self._creadas = max(0, self._creadas - 1)
            self._cond.notify()

    def devolver(self, conexion: Any) -> None:
        ahora = time.monotonic()
        with self._cond:
            if self._cerrado:
                self._creadas = max(0, self._creadas - 1)
                cerrar = True
            else:
                self._libres.append((conexion, ahora))
                self._cond.notify()
                cerrar = False
        if cerrar:
            try:
                conexion.close()
            except Exception:
                pass

    def descartar(self, conexion: Any) -> None:
        with self._cond:
            self._creadas = max(0, self._creadas - 1)
            self._cond.notify()
        try:
            conexion.close()
        except Exception:
            pass

    def cerrar(self) -> None:
        with self._cond:
            self._cerrado = True
            conexiones = list(self._libres)
            self._libres.clear()
            self._cond.notify_all()
        for conexion in conexiones:
            try:
                conexion.close()
            except Exception:
                pass

    @property
    def en_uso(self) -> int:
        with self._cond:
            return self._creadas - len(self._libres)


class Database:
    _pool: Optional[_PoolDeConexiones] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", "5432") or 5432)
        self.ssl = os.getenv("DB_SSL", "true").strip().lower() != "false"
        self.pool_min = max(1, int(os.getenv("DB_POOL_MIN", "5") or 5))
        self.pool_max = max(self.pool_min, int(os.getenv("DB_POOL_MAX", "15") or 15))
        self.pool_timeout = max(1, int(os.getenv("DB_POOL_TIMEOUT", "20") or 20))
        self.conn_max_idle = max(0, int(os.getenv("DB_CONN_MAX_IDLE", "120") or 120))

    def get_pool(self) -> _PoolDeConexiones:
        if Database._pool is None:
            with Database._lock:
                if Database._pool is None:
                    Database._pool = _PoolDeConexiones(
                        self.pool_max, self.pool_timeout
                    )
        return Database._pool

    def _abrir_conexion(self) -> Any:
        try:
            return psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password,
                sslmode="require" if self.ssl else "disable",
                connect_timeout=10,
            )
        except psycopg2.Error as exc:
            raise _error_503(MSG_SIN_CONEXION, "apertura de conexion", exc)

    def precalentar(self, cantidad: Optional[int] = None) -> int:
        objetivo = min(cantidad if cantidad is not None else self.pool_min, self.pool_max)
        pool_ = self.get_pool()
        hilos: list[threading.Thread] = []

        def abrir_y_guardar() -> None:
            conexion, _ociosa, hay_que_crear = pool_.reservar()
            if not hay_que_crear:
                pool_.devolver(conexion)
                return
            try:
                pool_.devolver(self._abrir_conexion())
            except Exception:
                pool_.cancelar_reserva()

        for _ in range(objetivo):
            hilo = threading.Thread(target=abrir_y_guardar, daemon=True)
            hilo.start()
            hilos.append(hilo)
        for hilo in hilos:
            hilo.join()
        return objetivo

    def _esta_viva(self, conexion: Any) -> bool:
        try:
            with conexion.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
            return True
        except Exception:
            return False

    def get_connection(self) -> ConexionPool:
        pool_ = self.get_pool()
        for _ in range(self.pool_max):
            conexion, ociosa_desde, hay_que_crear = pool_.reservar()
            if hay_que_crear:
                try:
                    raw = self._abrir_conexion()
                except Exception:
                    pool_.cancelar_reserva()
                    raise
                return ConexionPool(self, raw)
            if ociosa_desde and (time.monotonic() - ociosa_desde) <= self.conn_max_idle:
                return ConexionPool(self, conexion)
            if self._esta_viva(conexion):
                return ConexionPool(self, conexion)
            pool_.descartar(conexion)
        raw = self._abrir_conexion()
        return ConexionPool(self, raw)

    def release_connection(self, conn: Any) -> None:
        raw = conn._raw if isinstance(conn, ConexionPool) else conn
        pool_ = Database._pool
        if pool_ is None:
            try:
                raw.close()
            except Exception:
                pass
            return
        pool_.devolver(raw)

    def descartar_conexion(self, conn: Any) -> None:
        raw = conn._raw if isinstance(conn, ConexionPool) else conn
        pool_ = Database._pool
        if pool_ is None:
            try:
                raw.close()
            except Exception:
                pass
            return
        pool_.descartar(raw)

    def close_pool(self) -> None:
        with Database._lock:
            if Database._pool is not None:
                try:
                    Database._pool.cerrar()
                finally:
                    Database._pool = None

    def consultar(self, sql: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return [dict(fila) for fila in cur.fetchall()]

    def consultar_uno(self, sql: str, params: Optional[Sequence[Any]] = None) -> Optional[dict]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                fila = cur.fetchone()
                return dict(fila) if fila else None
