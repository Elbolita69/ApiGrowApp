from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.actuator import ActuatorCreate, ActuatorUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_ACTUATORS = """
    SELECT a.*,
           g.nombre AS greenhouse_nombre
    FROM actuators a
    JOIN greenhouses g ON a.greenhouse_id = g.id
"""


class ActuatorRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ACTUATORS + " WHERE a.estado = TRUE ORDER BY a.id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, actuator_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ACTUATORS + " WHERE a.estado = TRUE AND a.id = %s;",
                    (actuator_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_greenhouse(self, greenhouse_id: int) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM actuators WHERE estado = TRUE AND greenhouse_id = %s "
                    "ORDER BY id ASC;",
                    (greenhouse_id,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, actuator: ActuatorCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO actuators (greenhouse_id, tipo, nombre, ubicacion,
                       estado_actuador, estado)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        actuator.greenhouse_id,
                        actuator.tipo,
                        actuator.nombre,
                        actuator.ubicacion,
                        actuator.estado_actuador,
                        actuator.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, actuator_id: int, actuator: ActuatorUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "actuators",
                actuator.model_dump(exclude_unset=True),
                actuator_id,
            )

    def eliminar(self, actuator_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "actuators", actuator_id)
