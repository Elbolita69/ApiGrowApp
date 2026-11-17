from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.irrigation_log import IrrigationLogCreate, IrrigationLogUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_IRRIGATION_LOGS = """
    SELECT il.*,
           iz.nombre AS zone_nombre
    FROM irrigation_logs il
    JOIN irrigation_zones iz ON il.zone_id = iz.id
"""


class IrrigationLogRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self, limit: int = 100) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_IRRIGATION_LOGS
                    + " WHERE il.estado = TRUE ORDER BY il.creado DESC LIMIT %s;",
                    (limit,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, log_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_IRRIGATION_LOGS
                    + " WHERE il.estado = TRUE AND il.id = %s;",
                    (log_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_zone(self, zone_id: int, limit: int = 50) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM irrigation_logs WHERE estado = TRUE AND zone_id = %s "
                    "ORDER BY creado DESC LIMIT %s;",
                    (zone_id, limit),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, log: IrrigationLogCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO irrigation_logs (zone_id, duracion_minutos,
                       cantidad_agua_litros, modo, resultado, notas, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        log.zone_id,
                        log.duracion_minutos,
                        log.cantidad_agua_litros,
                        log.modo,
                        log.resultado,
                        log.notas,
                        log.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, registro_id: int, datos: IrrigationLogUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "irrigation_logs",
                datos.model_dump(exclude_unset=True),
                registro_id,
            )

    def eliminar(self, registro_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "irrigation_logs", registro_id)
