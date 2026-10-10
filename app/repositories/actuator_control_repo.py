from app.core.database import Database
from app.models.actuator_control import ActuatorControl, ActuatorControlCreate
from typing import Optional, List

class ActuatorControlRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self, limit: int = 100) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT ac.*, a.nombre as actuator_nombre, a.tipo as actuator_tipo,
                          u.username as usuario_username
                   FROM actuator_controls ac
                   JOIN actuators a ON ac.actuator_id = a.id
                   LEFT JOIN usuario u ON ac.usuario_id = u.id
                   ORDER BY ac.creado DESC LIMIT $1;""", limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, control_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """SELECT ac.*, a.nombre as actuator_nombre, u.username as usuario_username
                   FROM actuator_controls ac
                   JOIN actuators a ON ac.actuator_id = a.id
                   LEFT JOIN usuario u ON ac.usuario_id = u.id
                   WHERE ac.id = $1;""", control_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_actuator(self, actuator_id: int, limit: int = 50) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                """SELECT ac.*, u.username as usuario_username
                   FROM actuator_controls ac
                   LEFT JOIN usuario u ON ac.usuario_id = u.id
                   WHERE ac.actuator_id = $1
                   ORDER BY ac.creado DESC LIMIT $2;""", actuator_id, limit
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, control: ActuatorControlCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO actuator_controls (actuator_id, usuario_id, accion, valor_ajuste, resultado)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id;""",
                control.actuator_id, control.usuario_id, control.accion,
                control.valor_ajuste, control.resultado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)
