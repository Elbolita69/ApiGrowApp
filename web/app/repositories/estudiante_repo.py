from app.core.database import Database
from app.models.estudiante import Estudiante

class EstudianteRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self):
        conn = await self.db.get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM estudiantes ORDER BY id ASC;")
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, estudiante_id: int):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM estudiantes WHERE id = $1;", estudiante_id)
            return row
        finally:
            await self.db.release_connection(conn)

    async def crear(self, estudiante: Estudiante):
        conn = await self.db.get_connection()
        try:
            row = await conn.fetchrow(
                "INSERT INTO estudiantes (nombre, grado, promedio) VALUES ($1, $2, $3) RETURNING id;",
                estudiante.nombre, estudiante.grado, estudiante.promedio
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def eliminar(self, estudiante_id: int):
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow("DELETE FROM estudiantes WHERE id = $1 RETURNING id;", estudiante_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)

    async def actualizar(self, estudiante_id: int, estudiante: Estudiante):
        conn = await self.db.get_connection()
        try:
            result = await conn.fetchrow(
                "UPDATE estudiantes SET nombre = $1, grado = $2, promedio = $3 WHERE id = $4 RETURNING id;",
                estudiante.nombre, estudiante.grado, estudiante.promedio, estudiante_id
            )
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
