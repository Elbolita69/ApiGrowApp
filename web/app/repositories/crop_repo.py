from app.core.database import Database
from app.models.crop import Crop, CropCreate, CropUpdate
from typing import Optional, List

class CropRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM crops ORDER BY id ASC;")
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, crop_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM crops WHERE id = $1;", crop_id)
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, crop: CropCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO crops (nombre, nombre_cientifico, temperatura_min, temperatura_max,
                   humedad_min, humedad_max, ph_min, ph_max, ciclo_dias, descripcion)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id;""",
                crop.nombre, crop.nombre_cientifico, crop.temperatura_min, crop.temperatura_max,
                crop.humedad_min, crop.humedad_max, crop.ph_min, crop.ph_max, crop.ciclo_dias,
                crop.descripcion
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, crop_id: int, crop: CropUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("nombre", crop.nombre), ("nombre_cientifico", crop.nombre_cientifico),
                ("temperatura_min", crop.temperatura_min), ("temperatura_max", crop.temperatura_max),
                ("humedad_min", crop.humedad_min), ("humedad_max", crop.humedad_max),
                ("ph_min", crop.ph_min), ("ph_max", crop.ph_max),
                ("ciclo_dias", crop.ciclo_dias), ("descripcion", crop.descripcion)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(crop_id)
            query = f"UPDATE crops SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, crop_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM crops WHERE id = $1 RETURNING id;", crop_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
