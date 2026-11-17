from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.greenhouse_setting import (
    GreenhouseSettingCreate,
    GreenhouseSettingUpdate,
)
from app.repositories.crud_utils import (
    actualizar_generico,
    actualizar_generico_por_campo,
    eliminar_logico,
    eliminar_logico_por_campo,
)

SELECT_GREENHOUSE_SETTINGS = """
    SELECT gs.*,
           g.nombre AS greenhouse_nombre
    FROM greenhouse_settings gs
    JOIN greenhouses g ON gs.greenhouse_id = g.id
"""


class GreenhouseSettingRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_GREENHOUSE_SETTINGS
                    + " WHERE gs.estado = TRUE ORDER BY gs.id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, setting_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_GREENHOUSE_SETTINGS
                    + " WHERE gs.estado = TRUE AND gs.id = %s;",
                    (setting_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_greenhouse(self, greenhouse_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_GREENHOUSE_SETTINGS
                    + " WHERE gs.estado = TRUE AND gs.greenhouse_id = %s;",
                    (greenhouse_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, setting: GreenhouseSettingCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max,
                       humedad_min, humedad_max, luz_min, ph_min, ph_max,
                       intervalo_lectura_minutos, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        setting.greenhouse_id,
                        setting.temp_min,
                        setting.temp_max,
                        setting.humedad_min,
                        setting.humedad_max,
                        setting.luz_min,
                        setting.ph_min,
                        setting.ph_max,
                        setting.intervalo_lectura_minutos,
                        setting.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, setting_id: int, setting: GreenhouseSettingUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "greenhouse_settings",
                setting.model_dump(exclude_unset=True),
                setting_id,
            )

    def actualizar_por_greenhouse(
        self, greenhouse_id: int, setting: GreenhouseSettingUpdate
    ) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico_por_campo(
                conn,
                "greenhouse_settings",
                "greenhouse_id",
                greenhouse_id,
                setting.model_dump(exclude_unset=True),
            )

    def eliminar(self, setting_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "greenhouse_settings", setting_id)

    def eliminar_por_greenhouse(self, greenhouse_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico_por_campo(
                conn, "greenhouse_settings", "greenhouse_id", greenhouse_id
            )
