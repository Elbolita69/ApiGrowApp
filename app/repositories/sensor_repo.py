from app.core.database import Database
from app.models.sensor import Sensor, SensorCreate, SensorUpdate
from typing import Optional, List

class SensorRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM sensors ORDER BY id ASC;")
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, sensor_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM sensors WHERE id = $1;", sensor_id)
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_greenhouse(self, greenhouse_id: int) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT * FROM sensors WHERE greenhouse_id = $1 ORDER BY id ASC;", greenhouse_id
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, sensor: SensorCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO sensors (greenhouse_id, tipo, nombre, unidad, ubicacion, estado)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
                sensor.greenhouse_id, sensor.tipo, sensor.nombre, sensor.unidad,
                sensor.ubicacion, sensor.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, sensor_id: int, sensor: SensorUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            if sensor.greenhouse_id is not None:
                fields.append(f"greenhouse_id = ${idx}"); values.append(sensor.greenhouse_id); idx += 1
            if sensor.tipo is not None:
                fields.append(f"tipo = ${idx}"); values.append(sensor.tipo); idx += 1
            if sensor.nombre is not None:
                fields.append(f"nombre = ${idx}"); values.append(sensor.nombre); idx += 1
            if sensor.unidad is not None:
                fields.append(f"unidad = ${idx}"); values.append(sensor.unidad); idx += 1
            if sensor.ubicacion is not None:
                fields.append(f"ubicacion = ${idx}"); values.append(sensor.ubicacion); idx += 1
            if sensor.estado is not None:
                fields.append(f"estado = ${idx}"); values.append(sensor.estado); idx += 1

            if not fields:
                return False

            values.append(sensor_id)
            query = f"UPDATE sensors SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, sensor_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM sensors WHERE id = $1 RETURNING id;", sensor_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
