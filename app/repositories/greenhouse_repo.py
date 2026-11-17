from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.greenhouse import GreenhouseCreate, GreenhouseUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico


class GreenhouseRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM greenhouses WHERE estado = TRUE ORDER BY id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, greenhouse_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM greenhouses WHERE estado = TRUE AND id = %s;",
                    (greenhouse_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, greenhouse: GreenhouseCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO greenhouses (nombre, ubicacion, area_metros_cuadrados,
                       capacidad_maxima, estado)
                       VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        greenhouse.nombre,
                        greenhouse.ubicacion,
                        greenhouse.area_metros_cuadrados,
                        greenhouse.capacidad_maxima,
                        greenhouse.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, greenhouse_id: int, greenhouse: GreenhouseUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "greenhouses",
                greenhouse.model_dump(exclude_unset=True),
                greenhouse_id,
            )

    def eliminar(self, greenhouse_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "greenhouses", greenhouse_id)
