from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.alert import AlertCreate, AlertUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_ALERTS = """
    SELECT a.*,
           g.nombre AS greenhouse_nombre,
           s.nombre AS sensor_nombre
    FROM alerts a
    LEFT JOIN greenhouses g ON a.greenhouse_id = g.id
    LEFT JOIN sensors s ON a.sensor_id = s.id
"""


class AlertRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self, limit: int = 100) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ALERTS
                    + " WHERE a.estado = TRUE ORDER BY a.creado DESC LIMIT %s;",
                    (limit,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, alert_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ALERTS + " WHERE a.estado = TRUE AND a.id = %s;",
                    (alert_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_activas(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_ALERTS
                    + " WHERE a.estado = TRUE AND a.estado_alerta = 'activa' "
                    "ORDER BY a.creado DESC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, alert: AlertCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO alerts (greenhouse_id, sensor_id, tipo, mensaje,
                       valor_actual, umbral, prioridad, estado_alerta, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        alert.greenhouse_id,
                        alert.sensor_id,
                        alert.tipo,
                        alert.mensaje,
                        alert.valor_actual,
                        alert.umbral,
                        alert.prioridad,
                        alert.estado_alerta,
                        alert.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar_estado(self, alert_id: int, estado: str) -> bool:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if estado == "resuelta":
                    sql = (
                        "UPDATE alerts SET estado_alerta = %s, resuelta_en = CURRENT_TIMESTAMP, "
                        "actualizado = CURRENT_TIMESTAMP WHERE id = %s AND estado = TRUE "
                        "RETURNING id;"
                    )
                else:
                    sql = (
                        "UPDATE alerts SET estado_alerta = %s, actualizado = CURRENT_TIMESTAMP "
                        "WHERE id = %s AND estado = TRUE RETURNING id;"
                    )
                cur.execute(sql, (estado, alert_id))
                fila = cur.fetchone()
                return fila is not None

    def actualizar(self, registro_id: int, datos: AlertUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "alerts",
                datos.model_dump(exclude_unset=True),
                registro_id,
            )

    def eliminar(self, registro_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "alerts", registro_id)
