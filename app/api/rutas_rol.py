from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.core.database import Database

router = APIRouter(prefix="/roles", tags=["Roles"])
db = Database()


@router.get("/")
async def listar_roles(current_user: dict = Depends(get_current_user)):
    """Roles activos (para llenar listas desplegables)."""
    conn = await db.get_connection()
    try:
        rows = await conn.fetch("SELECT id, nombre, descripcion FROM rol WHERE estado = TRUE ORDER BY id;")
        return [dict(r) for r in rows]
    finally:
        await db.release_connection(conn)
