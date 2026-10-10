from app.core.database import Database
from app.models.irrigation_log import IrrigationLog, IrrigationLogCreate, IrrigationLogUpdate
from typing import Optional, List

class IrrigationLogRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self, limit: int = 100) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT il.*, iz.nombre as zone_nombre
                   FROM irrigation_logs il
                   JOIN irrigation_zones iz ON il.zone_id = iz.id
                   ORDER BY il.creado DESC LIMIT $1;""", limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, log_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT il.*, iz.nombre as zone_nombre
                   FROM irrigation_logs il
                   JOIN irrigation_zones iz ON il.zone_id = iz.id
                   WHERE il.id = $1;""", log_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_zone(self, zone_id: int, limit: int = 50) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT * FROM irrigation_logs WHERE zone_id = $1 ORDER BY creado DESC LIMIT $2;",
                zone_id, limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, log: IrrigationLogCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO irrigation_logs (zone_id, duracion_minutos, cantidad_agua_litros, modo, resultado, notas)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
                log.zone_id, log.duracion_minutos, log.cantidad_agua_litros,
                log.modo, log.resultado, log.notas
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)
