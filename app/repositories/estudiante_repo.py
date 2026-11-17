from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.estudiante import EstudianteCreate, EstudianteUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico


class EstudianteRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM estudiantes WHERE estado = TRUE ORDER BY id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, estudiante_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM estudiantes WHERE estado = TRUE AND id = %s;",
                    (estudiante_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, estudiante: EstudianteCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO estudiantes (nombre, grado, promedio, estado)
                       VALUES (%s, %s, %s, %s) RETURNING id;""",
                    (
                        estudiante.nombre,
                        estudiante.grado,
                        estudiante.promedio,
                        estudiante.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, estudiante_id: int, estudiante: EstudianteUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "estudiantes",
                estudiante.model_dump(exclude_unset=True),
                estudiante_id,
            )

    def eliminar(self, estudiante_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "estudiantes", estudiante_id)
