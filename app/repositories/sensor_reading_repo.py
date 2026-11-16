"""Repositorio de lecturas de sensores (SQL puro con psycopg2, sincrono)."""

from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.sensor_reading import SensorReadingCreate, SensorReadingUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

# JOIN con alias legibles: el frontend nunca necesita conocer ids.
SELECT_SENSOR_READINGS = """
    SELECT sr.*,
           s.nombre AS sensor_nombre,
           s.tipo   AS sensor_tipo,
           s.unidad AS sensor_unidad,
           s.tipo   AS tipo,
           s.unidad AS unidad
    FROM sensor_readings sr
    JOIN sensors s ON sr.sensor_id = s.id
"""


class SensorReadingRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self, limit: int = 100) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_SENSOR_READINGS
                    + " WHERE sr.estado = TRUE ORDER BY sr.timestamp DESC LIMIT %s;",
                    (limit,),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, reading_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_SENSOR_READINGS
                    + " WHERE sr.estado = TRUE AND sr.id = %s;",
                    (reading_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_sensor(self, sensor_id: int, limit: int = 50) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_SENSOR_READINGS
                    + " WHERE sr.estado = TRUE AND sr.sensor_id = %s "
                    "ORDER BY sr.timestamp DESC LIMIT %s;",
                    (sensor_id, limit),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_ultimas_lecturas(
        self, greenhouse_id: int, limit: int = 20
    ) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_SENSOR_READINGS
                    + " WHERE sr.estado = TRUE AND s.greenhouse_id = %s "
                    "ORDER BY sr.timestamp DESC LIMIT %s;",
                    (greenhouse_id, limit),
                )
                return [dict(fila) for fila in cur.fetchall()]

    def crear(self, reading: SensorReadingCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO sensor_readings (sensor_id, valor, estado)
                       VALUES (%s, %s, %s) RETURNING id;""",
                    (reading.sensor_id, reading.valor, reading.estado),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, registro_id: int, datos: SensorReadingUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "sensor_readings",
                datos.model_dump(exclude_unset=True),
                registro_id,
            )

    def eliminar(self, registro_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "sensor_readings", registro_id)
