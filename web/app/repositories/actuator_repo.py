from app.core.database import Database
from app.models.actuator import Actuator, ActuatorCreate, ActuatorUpdate
from typing import Optional, List

class ActuatorRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT a.*, g.nombre as greenhouse_nombre
                   FROM actuators a
                   JOIN greenhouses g ON a.greenhouse_id = g.id
                   ORDER BY a.id ASC;"""
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, actuator_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT a.*, g.nombre as greenhouse_nombre
                   FROM actuators a
                   JOIN greenhouses g ON a.greenhouse_id = g.id
                   WHERE a.id = $1;""", actuator_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_greenhouse(self, greenhouse_id: int) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT * FROM actuators WHERE greenhouse_id = $1 ORDER BY id ASC;", greenhouse_id
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, actuator: ActuatorCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO actuators (greenhouse_id, tipo, nombre, ubicacion, estado)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id;""",
                actuator.greenhouse_id, actuator.tipo, actuator.nombre,
                actuator.ubicacion, actuator.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, actuator_id: int, actuator: ActuatorUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("greenhouse_id", actuator.greenhouse_id), ("tipo", actuator.tipo),
                ("nombre", actuator.nombre), ("ubicacion", actuator.ubicacion),
                ("estado", actuator.estado)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(actuator_id)
            query = f"UPDATE actuators SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, actuator_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM actuators WHERE id = $1 RETURNING id;", actuator_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
