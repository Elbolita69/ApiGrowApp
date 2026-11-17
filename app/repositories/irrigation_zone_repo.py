from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.irrigation_zone import IrrigationZoneCreate, IrrigationZoneUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_IRRIGATION_ZONES = """
    SELECT iz.*,
           g.nombre AS greenhouse_nombre
    FROM irrigation_zones iz
    JOIN greenhouses g ON iz.greenhouse_id = g.id
"""


class IrrigationZoneRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_IRRIGATION_ZONES
                    + " WHERE iz.estado = TRUE ORDER BY iz.id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, zone_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_IRRIGATION_ZONES
                    + " WHERE iz.estado = TRUE AND iz.id = %s;",
                    (zone_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_greenhouse(self, greenhouse_id: int) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM irrigation_zones WHERE estado = TRUE AND greenhouse_id = %s "
                    "ORDER BY id ASC;",
                    (greenhouse_id,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, zone: IrrigationZoneCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO irrigation_zones (greenhouse_id, nombre,
                       capacidad_litros_min, capacidad_litros_max, tipo, estado)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        zone.greenhouse_id,
                        zone.nombre,
                        zone.capacidad_litros_min,
                        zone.capacidad_litros_max,
                        zone.tipo,
                        zone.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, zone_id: int, zone: IrrigationZoneUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "irrigation_zones",
                zone.model_dump(exclude_unset=True),
                zone_id,
            )

    def eliminar(self, zone_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "irrigation_zones", zone_id)
