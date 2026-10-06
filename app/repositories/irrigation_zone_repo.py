from app.core.database import Database
from app.models.irrigation_zone import IrrigationZone, IrrigationZoneCreate, IrrigationZoneUpdate
from typing import Optional, List

class IrrigationZoneRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT iz.*, g.nombre as greenhouse_nombre
                   FROM irrigation_zones iz
                   JOIN greenhouses g ON iz.greenhouse_id = g.id
                   ORDER BY iz.id ASC;"""
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, zone_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT iz.*, g.nombre as greenhouse_nombre
                   FROM irrigation_zones iz
                   JOIN greenhouses g ON iz.greenhouse_id = g.id
                   WHERE iz.id = $1;""", zone_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_greenhouse(self, greenhouse_id: int) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT * FROM irrigation_zones WHERE greenhouse_id = $1 ORDER BY id ASC;", greenhouse_id
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, zone: IrrigationZoneCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO irrigation_zones (greenhouse_id, nombre, capacidadLitros_min, capacidadLitros_max, tipo, estado)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
                zone.greenhouse_id, zone.nombre, zone.capacidadLitros_min,
                zone.capacidadLitros_max, zone.tipo, zone.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, zone_id: int, zone: IrrigationZoneUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("greenhouse_id", zone.greenhouse_id), ("nombre", zone.nombre),
                ("capacidadLitros_min", zone.capacidadLitros_min), ("capacidadLitros_max", zone.capacidadLitros_max),
                ("tipo", zone.tipo), ("estado", zone.estado)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(zone_id)
            query = f"UPDATE irrigation_zones SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, zone_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM irrigation_zones WHERE id = $1 RETURNING id;", zone_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
