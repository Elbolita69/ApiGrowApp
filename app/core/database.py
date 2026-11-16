import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()


class Database:
    """Acceso a PostgreSQL. Todas las instancias comparten UN solo pool de conexiones
    (importante en Neon, que limita las conexiones, y para evitar que peticiones
    simultaneas creen pools duplicados)."""

    _pool = None
    _lock = None

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT", "5432")
        # DB_SSL=false para la base de datos local; en la nube (Neon) se deja en true
        self.ssl = os.getenv("DB_SSL", "true").lower() != "false"

    async def get_pool(self):
        if Database._pool is None:
            if Database._lock is None:
                Database._lock = asyncio.Lock()
            async with Database._lock:
                if Database._pool is None:
                    Database._pool = await asyncpg.create_pool(
                        host=self.host,
                        database=self.database,
                        user=self.user,
                        password=self.password,
                        port=int(self.port),
                        command_timeout=60,
                        ssl=self.ssl,
                    )
        return Database._pool

    async def get_connection(self):
        pool = await self.get_pool()
        return await pool.acquire()

    async def release_connection(self, conn):
        pool = await self.get_pool()
        await pool.release(conn)

    async def close(self):
        if Database._pool:
            await Database._pool.close()
            Database._pool = None
