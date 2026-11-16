"""Repositorio de cultivos (SQL puro con psycopg2, sincrono)."""

from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.crop import CropCreate, CropUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico


class CropRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM crops WHERE estado = TRUE ORDER BY id ASC;")
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, crop_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM crops WHERE estado = TRUE AND id = %s;",
                    (crop_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, crop: CropCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO crops (nombre, nombre_cientifico, temperatura_min,
                       temperatura_max, humedad_min, humedad_max, ph_min, ph_max,
                       ciclo_dias, descripcion, estado)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       RETURNING id;""",
                    (
                        crop.nombre,
                        crop.nombre_cientifico,
                        crop.temperatura_min,
                        crop.temperatura_max,
                        crop.humedad_min,
                        crop.humedad_max,
                        crop.ph_min,
                        crop.ph_max,
                        crop.ciclo_dias,
                        crop.descripcion,
                        crop.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, crop_id: int, crop: CropUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "crops",
                crop.model_dump(exclude_unset=True),
                crop_id,
            )

    def eliminar(self, crop_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "crops", crop_id)
