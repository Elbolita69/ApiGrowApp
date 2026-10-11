from app.core.database import Database
from app.models.greenhouse import Greenhouse, GreenhouseCreate, GreenhouseUpdate
from typing import Optional, List

class GreenhouseRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM greenhouses ORDER BY id ASC;")
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, greenhouse_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM greenhouses WHERE id = $1;", greenhouse_id)
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, greenhouse: GreenhouseCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO greenhouses (nombre, ubicacion, area_metros_cuadrados, capacidad_maxima, estado)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id;""",
                greenhouse.nombre, greenhouse.ubicacion, greenhouse.area_metros_cuadrados,
                greenhouse.capacidad_maxima, greenhouse.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, greenhouse_id: int, greenhouse: GreenhouseUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            if greenhouse.nombre is not None:
                fields.append(f"nombre = ${idx}"); values.append(greenhouse.nombre); idx += 1
            if greenhouse.ubicacion is not None:
                fields.append(f"ubicacion = ${idx}"); values.append(greenhouse.ubicacion); idx += 1
            if greenhouse.area_metros_cuadrados is not None:
                fields.append(f"area_metros_cuadrados = ${idx}"); values.append(greenhouse.area_metros_cuadrados); idx += 1
            if greenhouse.capacidad_maxima is not None:
                fields.append(f"capacidad_maxima = ${idx}"); values.append(greenhouse.capacidad_maxima); idx += 1
            if greenhouse.estado is not None:
                fields.append(f"estado = ${idx}"); values.append(greenhouse.estado); idx += 1

            if not fields:
                return False

            values.append(greenhouse_id)
            query = f"UPDATE greenhouses SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, greenhouse_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM greenhouses WHERE id = $1 RETURNING id;", greenhouse_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
