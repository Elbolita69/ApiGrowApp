from app.core.database import Database
from app.core.auth import get_password_hash
from app.models.user import User, UserCreate, UserUpdate
from typing import Optional, List

class UserRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT id, username, email, nombre, rol_id, estado, creado FROM usuario WHERE estado = TRUE ORDER BY id ASC;"
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, user_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT id, username, email, nombre, rol_id, estado, creado FROM usuario WHERE estado = TRUE AND id = $1;", user_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_username(self, username: str):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM usuario WHERE estado = TRUE AND username = $1;", username)
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, user: UserCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO usuario (username, email, password_hash, nombre, rol_id, estado)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
                user.username, user.email, get_password_hash(user.password), user.nombre, user.rol_id, user.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, user_id: int, user: UserUpdate) -> bool:
        conn = await self.db.get_connection()
        try:
            fields = []
            values = []
            idx = 1

            for field, value in [
                ("username", user.username), ("email", user.email),
                ("nombre", user.nombre), ("rol_id", user.rol_id), ("estado", user.estado)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if user.password:
                fields.append(f"password_hash = ${idx}"); values.append(get_password_hash(user.password)); idx += 1

            if not fields:
                return False

            values.append(user_id)
            query = f"UPDATE usuario SET {', '.join(fields)}, actualizado = CURRENT_TIMESTAMP WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, user_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("UPDATE usuario SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id = $1 AND estado = TRUE RETURNING id;", user_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
