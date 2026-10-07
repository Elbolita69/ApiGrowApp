import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self._pool = None

    async def get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                self.database_url,
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
