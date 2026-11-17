from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.actuator_control import ActuatorControlCreate, ActuatorControlUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_ACTUATOR_CONTROLS = """
    SELECT ac.*,
           a.nombre AS actuator_nombre,
           a.tipo   AS actuator_tipo,
           u.username AS usuario_username
    FROM actuator_controls ac
    JOIN actuators a ON ac.actuator_id = a.id
    LEFT JOIN usuario u ON ac.usuario_id = u.id
"""


class ActuatorControlRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self, limit: int = 100) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ACTUATOR_CONTROLS
                    + " WHERE ac.estado = TRUE ORDER BY ac.creado DESC LIMIT %s;",
                    (limit,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, control_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ACTUATOR_CONTROLS
                    + " WHERE ac.estado = TRUE AND ac.id = %s;",
                    (control_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_actuator(self, actuator_id: int, limit: int = 50) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ACTUATOR_CONTROLS
                    + " WHERE ac.estado = TRUE AND ac.actuator_id = %s "
                    "ORDER BY ac.creado DESC LIMIT %s;",
                    (actuator_id, limit),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(
        self, control: ActuatorControlCreate, usuario_id: Optional[int] = None
    ) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO actuator_controls (actuator_id, usuario_id, accion,
                       valor_ajuste, resultado, estado)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        control.actuator_id,
                        usuario_id,
                        control.accion,
                        control.valor_ajuste,
                        control.resultado,
                        control.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, registro_id: int, datos: ActuatorControlUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "actuator_controls",
                datos.model_dump(exclude_unset=True),
                registro_id,
            )

    def eliminar(self, registro_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "actuator_controls", registro_id)
