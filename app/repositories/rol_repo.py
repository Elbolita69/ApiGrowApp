"""Repositorio de roles (SQL puro con psycopg2, sincrono).

El nombre del rol es la clave de negocio: administrador, supervisor, agronomo,
regador, tecnico, auxiliar_riego, planificador, calidad, mantenimiento, lector.
"""

from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.database import Database
from app.models.rol import RolCreate, RolUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico


class RolRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, nombre, descripcion, estado, creado, actualizado "
                    "FROM rol WHERE estado = TRUE ORDER BY id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, rol_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, nombre, descripcion, estado, creado, actualizado "
                    "FROM rol WHERE estado = TRUE AND id = %s;",
                    (rol_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_nombre(self, nombre: str) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, nombre, descripcion, estado, creado, actualizado "
                    "FROM rol WHERE estado = TRUE AND nombre = %s;",
                    (nombre,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, rol: RolCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO rol (nombre, descripcion, estado) VALUES (%s, %s, %s) "
                    "RETURNING id;",
                    (rol.nombre, rol.descripcion, rol.estado),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, rol_id: int, rol: RolUpdate) -> bool:
        with self.db.get_connection() as conn:
            return actualizar_generico(
                conn,
                "rol",
                rol.model_dump(exclude_unset=True),
                rol_id,
            )

    def eliminar(self, rol_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "rol", rol_id)
