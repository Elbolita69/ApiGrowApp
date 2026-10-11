import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT")
        self._pool = None

    async def get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                command_timeout=60
            )
        return self._pool

    async def get_connection(self):
        pool = await self.get_pool()
        return await pool.acquire()

    async def release_connection(self, conn):
        pool = await self.get_pool()
        await pool.release(conn)

    async def close(self):
        if self._pool:
            await self._pool.close()
