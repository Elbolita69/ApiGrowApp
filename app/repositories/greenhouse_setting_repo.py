from app.core.database import Database
from app.models.greenhouse_setting import GreenhouseSetting, GreenhouseSettingCreate, GreenhouseSettingUpdate
from typing import Optional, List

class GreenhouseSettingRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT gs.*, g.nombre as greenhouse_nombre
                   FROM greenhouse_settings gs
                   JOIN greenhouses g ON gs.greenhouse_id = g.id
                   ORDER BY gs.id ASC;"""
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, setting_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT gs.*, g.nombre as greenhouse_nombre
                   FROM greenhouse_settings gs
                   JOIN greenhouses g ON gs.greenhouse_id = g.id
                   WHERE gs.id = $1;""", setting_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_greenhouse(self, greenhouse_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM greenhouse_settings WHERE greenhouse_id = $1;", greenhouse_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, setting: GreenhouseSettingCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max, humedad_min,
                   humedad_max, luz_min, ph_min, ph_max, intervalo_lectura_minutos)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id;""",
                setting.greenhouse_id, setting.temp_min, setting.temp_max, setting.humedad_min,
                setting.humedad_max, setting.luz_min, setting.ph_min, setting.ph_max,
                setting.intervalo_lectura_minutos
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, greenhouse_id: int, setting: GreenhouseSettingUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("temp_min", setting.temp_min), ("temp_max", setting.temp_max),
                ("humedad_min", setting.humedad_min), ("humedad_max", setting.humedad_max),
                ("luz_min", setting.luz_min), ("ph_min", setting.ph_min),
                ("ph_max", setting.ph_max), ("intervalo_lectura_minutos", setting.intervalo_lectura_minutos)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(greenhouse_id)
            query = f"UPDATE greenhouse_settings SET {', '.join(fields)}, actualizado_en = CURRENT_TIMESTAMP WHERE greenhouse_id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
