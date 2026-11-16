"""Acceso a PostgreSQL con psycopg2 (driver sincrono).

Decisiones del taller:
- El driver es `psycopg2` (sincrono). Por eso los routers usan handlers
  sincronos (`def`): FastAPI los ejecuta en su threadpool y una conexion nunca
  se comparte entre hilos.
- Las conexiones se toman de un pool propio y se devuelven al salir del bloque
  `with`. Nunca se usa una conexion global.
- El borrado es logico (`estado = FALSE`); aqui no hay ninguna sentencia de
  borrado fisico.
"""

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
            # La transaccion no pudo cerrarse: la conexion esta rota (el
            # servidor la cerro mientras estaba ociosa). Se descarta en vez
            # de devolverla al pool, para no reciclar una conexion muerta.
            logger.warning("Conexion descartada al cerrarla: %s", _sanear(str(exc)))
            self._db.descartar_conexion(raw)
            return
        self._db.release_connection(raw)

    def __getattr__(self, nombre: str) -> Any:
        # Delegacion transparente hacia la conexion cruda de psycopg2.
        if nombre.startswith("__") or nombre in ("_db", "_raw", "_cerrada"):
            raise AttributeError(nombre)
        return getattr(self._raw, nombre)


class _PoolDeConexiones:
    """Pool propio de conexiones a PostgreSQL.

    Se implementa a mano en vez de usar `psycopg2.pool.ThreadedConnectionPool`
    por dos motivos que solo aparecen contra una base en la nube:

    1. `getconn()` no espera: si no hay conexion libre lanza `PoolError` de
       inmediato y la API responde 503 aunque la base este disponible.
       Aqui la peticion **espera** a que se libere una conexion.
    2. `ThreadedConnectionPool` abre las conexiones de una en una. En Neon
       cada conexion tarda ~0.6 s en establecerse, asi que 13 modulos en
       paralelo tardaban mas de 10 segundos. Aqui las conexiones nuevas se
       crean **en paralelo** y el pool se precalienta al arrancar.
    """

    def __init__(self, maximo: int, timeout: int) -> None:
        self.maximo = maximo
        self.timeout = timeout
        self._libres: list[tuple[Any, float]] = []
        self._creadas = 0
        self._cerrado = False
        self._cond = threading.Condition()

    # ------------------------------------------------------------- turnos
    def reservar(self) -> tuple[Optional[Any], float, bool]:
        """Reserva un turno.

        Devuelve `(conexion, ociosa_desde, hay_que_crear)`. Si hay una conexion
        libre se entrega con el momento en que se devolvio al pool, para
        poder saber si lleva demasiado tiempo ociosa. Si no hay ninguna y
        todavia hay cupo, se devuelve `hay_que_crear=True`: el que llama
        abre la conexion FUERA del lock para que varias peticiones puedan
        hacerlo a la vez.
        """
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
        """Devuelve el turno si la conexion no se pudo abrir."""
        with self._cond:
            self._creadas = max(0, self._creadas - 1)
            self._cond.notify()

    def devolver(self, conexion: Any) -> None:
        """Devuelve una conexion al pool."""
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
            except Exception:  # pragma: no cover - la conexion ya no sirve
                pass

    def descartar(self, conexion: Any) -> None:
        """Elimina una conexion rota del pool y libera su cupo."""
        with self._cond:
            self._creadas = max(0, self._creadas - 1)
            self._cond.notify()
        try:
            conexion.close()
        except Exception:  # pragma: no cover - la conexion ya no sirve
            pass

    def cerrar(self) -> None:
        """Cierra el pool y todas sus conexiones."""
        with self._cond:
            self._cerrado = True
            conexiones = list(self._libres)
            self._libres.clear()
            self._cond.notify_all()
        for conexion in conexiones:
            try:
                conexion.close()
            except Exception:  # pragma: no cover
                pass

    @property
    def en_uso(self) -> int:
        with self._cond:
            return self._creadas - len(self._libres)


class Database:
    """Pool de conexiones a PostgreSQL (psycopg2, sincrono).

    Todas las instancias comparten un unico pool (importante en Neon, que
    limita el numero de conexiones simultaneas).
    """

    _pool: Optional[_PoolDeConexiones] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", "5432") or 5432)
        # DB_SSL=false para una base local; en la nube (Neon) se deja en true
        self.ssl = os.getenv("DB_SSL", "true").strip().lower() != "false"
        self.pool_min = max(1, int(os.getenv("DB_POOL_MIN", "5") or 5))
        self.pool_max = max(self.pool_min, int(os.getenv("DB_POOL_MAX", "15") or 15))
        # Espera maxima por una conexion libre (segundos).
        self.pool_timeout = max(1, int(os.getenv("DB_POOL_TIMEOUT", "20") or 20))
        # Tiempo maximo que una conexion puede quedar ociosa en el pool antes
        # de comprobar que sigue viva (el servidor puede haberla cerrado).
        self.conn_max_idle = max(0, int(os.getenv("DB_CONN_MAX_IDLE", "120") or 120))

    # ------------------------------------------------------------------ pool
    def get_pool(self) -> _PoolDeConexiones:
        """Devuelve (creandolo si hace falta) el pool de conexiones."""
        if Database._pool is None:
            with Database._lock:
                if Database._pool is None:
                    Database._pool = _PoolDeConexiones(
                        self.pool_max, self.pool_timeout
                    )
        return Database._pool

    def _abrir_conexion(self) -> Any:
        """Abre una conexion nueva a PostgreSQL."""
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
        """Abre conexiones en paralelo y las deja listas en el pool.

        Se usa al arrancar la API: en Neon abrir una conexion tarda ~0.6 s y
        hacerlo en serie retrasaria la primera peticion del usuario.
        """
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
        """Comprueba que la conexion sigue viva con un SELECT 1."""
        try:
            with conexion.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
            return True
        except Exception:
            return False

    def get_connection(self) -> ConexionPool:
        """Toma una conexion del pool (usable como context manager).

        Una conexion que lleva mucho tiempo ociosa puede haber sido cerrada
        por el servidor (Neon cierra las conexiones inactivas y Render duerme
        las instancias). Si eso paso, se descarta y se prueba con otra en
        lugar de fallar con un 503.
        """
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
                # Recien usada: se supone que sigue viva.
                return ConexionPool(self, conexion)
            if self._esta_viva(conexion):
                return ConexionPool(self, conexion)
            # La conexion murio: se descarta y se prueba con otra.
            pool_.descartar(conexion)
        # Ninguna conexion del pool sirvio: se abre una nueva.
        raw = self._abrir_conexion()
        return ConexionPool(self, raw)

    def release_connection(self, conn: Any) -> None:
        """Devuelve una conexion al pool."""
        raw = conn._raw if isinstance(conn, ConexionPool) else conn
        pool_ = Database._pool
        if pool_ is None:
            try:
                raw.close()
            except Exception:  # pragma: no cover
                pass
            return
        pool_.devolver(raw)

    def descartar_conexion(self, conn: Any) -> None:
        """Saca una conexion rota del pool (no vuelve a reciclarce)."""
        raw = conn._raw if isinstance(conn, ConexionPool) else conn
        pool_ = Database._pool
        if pool_ is None:
            try:
                raw.close()
            except Exception:  # pragma: no cover
                pass
            return
        pool_.descartar(raw)

    def close_pool(self) -> None:
        """Cierra el pool y todas sus conexiones."""
        with Database._lock:
            if Database._pool is not None:
                try:
                    Database._pool.cerrar()
                finally:
                    Database._pool = None

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
