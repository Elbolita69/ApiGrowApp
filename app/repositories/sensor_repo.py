"""Repositorio de sensores (SQL puro con psycopg2, sincrono)."""

from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.sensor import SensorCreate, SensorUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico


class SensorRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM sensors WHERE estado = TRUE ORDER BY id ASC;")
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, sensor_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM sensors WHERE estado = TRUE AND id = %s;",
                    (sensor_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_greenhouse(self, greenhouse_id: int) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM sensors WHERE estado = TRUE AND greenhouse_id = %s "
                    "ORDER BY id ASC;",
                    (greenhouse_id,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, sensor: SensorCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO sensors (greenhouse_id, tipo, nombre, unidad, ubicacion, estado)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        sensor.greenhouse_id,
                        sensor.tipo,
                        sensor.nombre,
                        sensor.unidad,
                        sensor.ubicacion,
                        sensor.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, sensor_id: int, sensor: SensorUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "sensors",
                sensor.model_dump(exclude_unset=True),
                sensor_id,
            )

    def eliminar(self, sensor_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "sensors", sensor_id)
