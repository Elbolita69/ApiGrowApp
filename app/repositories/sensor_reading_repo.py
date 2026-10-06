from app.core.database import Database
from app.models.sensor_reading import SensorReading, SensorReadingCreate
from typing import Optional, List

class SensorReadingRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT sr.*, s.nombre as sensor_nombre, s.tipo, s.unidad "
                "FROM sensor_readings sr "
                "JOIN sensors s ON sr.sensor_id = s.id "
                "ORDER BY sr.timestamp DESC LIMIT 100;"
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, reading_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM sensor_readings WHERE id = $1;", reading_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_sensor(self, sensor_id: int, limit: int = 50) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT * FROM sensor_readings WHERE sensor_id = $1 ORDER BY timestamp DESC LIMIT $2;",
                sensor_id, limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, reading: SensorReadingCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "INSERT INTO sensor_readings (sensor_id, valor) VALUES ($1, $2) RETURNING id;",
                reading.sensor_id, reading.valor
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def obtener_ultimas_lecturas(self, greenhouse_id: int, limit: int = 20) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT sr.*, s.nombre as sensor_nombre, s.tipo, s.unidad
                   FROM sensor_readings sr
                   JOIN sensors s ON sr.sensor_id = s.id
                   WHERE s.greenhouse_id = $1
                   ORDER BY sr.timestamp DESC LIMIT $2;""",
                greenhouse_id, limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)
