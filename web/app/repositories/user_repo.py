from app.core.database import Database
from app.models.user import User, UserCreate, UserUpdate
from typing import Optional, List

class UserRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch(
                "SELECT id, username, email, nombre, rol, estado, fecha_registro FROM users ORDER BY id ASC;"
            )
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, user_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT id, username, email, nombre, rol, estado, fecha_registro FROM users WHERE id = $1;", user_id
            )
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_username(self, username: str):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM users WHERE username = $1;", username)
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, user: UserCreate) -> int:
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO users (username, email, password_hash, nombre, rol, estado)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;""",
                user.username, user.email, user.password, user.nombre, user.rol, user.estado
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
                ("nombre", user.nombre), ("rol", user.rol), ("estado", user.estado)
            ]:
                if value is not None:
                    fields.append(f"{field} = ${idx}"); values.append(value); idx += 1

            if not fields:
                return False

            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ${idx} RETURNING id;"
            result = await conn.fetchrow(query, *values)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, user_id: int) -> bool:
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM users WHERE id = $1 RETURNING id;", user_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
