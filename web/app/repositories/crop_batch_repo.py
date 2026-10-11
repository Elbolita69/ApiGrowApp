from app.core.database import Database
from app.models.crop_batch import CropBatch, CropBatchCreate, CropBatchUpdate
from typing import Optional, List

class CropBatchRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT cb.*, c.nombre as cultivo_nombre
                   FROM crop_batches cb
                   LEFT JOIN crops c ON cb.crop_id = c.id
                   ORDER BY cb.fecha_siembra DESC;"""
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, batch_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT cb.*, c.nombre as cultivo_nombre
                   FROM crop_batches cb
                   LEFT JOIN crops c ON cb.crop_id = c.id
                   WHERE cb.id = $1;""", batch_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_greenhouse(self, greenhouse_id: int) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT cb.*, c.nombre as cultivo_nombre
                   FROM crop_batches cb
                   LEFT JOIN crops c ON cb.crop_id = c.id
                   WHERE cb.greenhouse_id = $1
                   ORDER BY cb.fecha_siembra DESC;""", greenhouse_id
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, batch: CropBatchCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO crop_batches (crop_id, greenhouse_id, fecha_siembra, fecha_cosecha_estimada,
                   cantidad_plantas, estado, notas)
                   VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;""",
                batch.crop_id, batch.greenhouse_id, batch.fecha_siembra,
                batch.fecha_cosecha_estimada, batch.cantidad_plantas, batch.estado, batch.notas
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, batch_id: int, batch: CropBatchUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("crop_id", batch.crop_id), ("greenhouse_id", batch.greenhouse_id),
                ("fecha_siembra", batch.fecha_siembra), ("fecha_cosecha_estimada", batch.fecha_cosecha_estimada),
                ("fecha_cosecha_real", batch.fecha_cosecha_real), ("cantidad_plantas", batch.cantidad_plantas),
                ("estado", batch.estado), ("notas", batch.notas)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(batch_id)
            query = f"UPDATE crop_batches SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, batch_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM crop_batches WHERE id = $1 RETURNING id;", batch_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
