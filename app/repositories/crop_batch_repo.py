from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.crop_batch import CropBatchCreate, CropBatchUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_CROP_BATCHES = """
    SELECT cb.*,
           c.nombre AS crop_nombre,
           g.nombre AS greenhouse_nombre,
           c.nombre AS cultivo_nombre
    FROM crop_batches cb
    LEFT JOIN crops c ON cb.crop_id = c.id
    LEFT JOIN greenhouses g ON cb.greenhouse_id = g.id
"""


class CropBatchRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_CROP_BATCHES
                    + " WHERE cb.estado = TRUE ORDER BY cb.fecha_siembra DESC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, batch_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_CROP_BATCHES
                    + " WHERE cb.estado = TRUE AND cb.id = %s;",
                    (batch_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_greenhouse(self, greenhouse_id: int) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_CROP_BATCHES
                    + " WHERE cb.estado = TRUE AND cb.greenhouse_id = %s "
                    "ORDER BY cb.fecha_siembra DESC;",
                    (greenhouse_id,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, batch: CropBatchCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO crop_batches (crop_id, greenhouse_id, fecha_siembra,
                       fecha_cosecha_estimada, fecha_cosecha_real, cantidad_plantas,
                       estado_cultivo, notas, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        batch.crop_id,
                        batch.greenhouse_id,
                        batch.fecha_siembra,
                        batch.fecha_cosecha_estimada,
                        batch.fecha_cosecha_real,
                        batch.cantidad_plantas,
                        batch.estado_cultivo,
                        batch.notas,
                        batch.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, batch_id: int, batch: CropBatchUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "crop_batches",
                batch.model_dump(exclude_unset=True),
                batch_id,
            )

    def eliminar(self, batch_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "crop_batches", batch_id)
