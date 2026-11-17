from __future__ import annotations

from typing import Optional

from psycopg2.extras import RealDictCursor

from app.core.auth import get_password_hash
from app.core.database import Database
from app.models.user import UserCreate, UserUpdate
from app.repositories.crud_utils import actualizar_generico, eliminar_logico

SELECT_USUARIOS = """
    SELECT u.id,
           u.username,
           u.email,
           u.nombre,
           u.rol_id,
           r.nombre AS rol_nombre,
           u.estado,
           u.creado,
           u.actualizado
    FROM usuario u
    LEFT JOIN rol r ON u.rol_id = r.id
"""


class UserRepository:
    def __init__(self) -> None:
        self.db = Database()

    def obtener_todos(self) -> list[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_USUARIOS + " WHERE u.estado = TRUE ORDER BY u.id ASC;"
                )
                return [dict(fila) for fila in cur.fetchall()]

    def obtener_por_id(self, user_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_USUARIOS + " WHERE u.estado = TRUE AND u.id = %s;",
                    (user_id,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_username(self, username: str) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    SELECT_USUARIOS + " WHERE u.estado = TRUE AND u.username = %s;",
                    (username,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_credenciales_por_username(self, username: str) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """SELECT u.id, u.username, u.email, u.nombre, u.password_hash,
                       u.rol_id, u.estado, r.nombre AS rol_nombre
                       FROM usuario u
                       LEFT JOIN rol r ON u.rol_id = r.id
                       WHERE u.username = %s;""",
                    (username,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def obtener_por_rol(self, rol_nombre: str) -> Optional[dict]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id FROM rol WHERE nombre = %s AND estado = TRUE;",
                    (rol_nombre,),
                )
                fila = cur.fetchone()
                return dict(fila) if fila else None

    def crear(self, user: UserCreate) -> Optional[int]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """INSERT INTO usuario (username, email, password_hash, nombre,
                       rol_id, estado)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                    (
                        user.username,
                        user.email,
                        get_password_hash(user.password),
                        user.nombre,
                        user.rol_id,
                        user.estado,
                    ),
                )
                fila = cur.fetchone()
                return fila["id"] if fila else None

    def actualizar(self, user_id: int, user: UserUpdate) -> bool:
        datos = user.model_dump(exclude_unset=True)
        if datos.get("password"):
            datos["password_hash"] = get_password_hash(datos.pop("password"))
        with self.db.get_connection() as conn:
            return actualizar_generico(conn, "usuario", datos, user_id)

    def eliminar(self, user_id: int) -> bool:
        with self.db.get_connection() as conn:
            return eliminar_logico(conn, "usuario", user_id)
