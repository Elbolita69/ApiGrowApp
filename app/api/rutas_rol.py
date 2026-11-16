from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.repositories.rol_repo import RolRepository

router = APIRouter(prefix="/roles", tags=["Roles"])
repo = RolRepository()


@router.get("/")
def listar_roles(current_user: dict = Depends(get_current_user)):
    """Roles activos (para llenar las listas desplegables del formulario de usuario)."""
    return [
        {"id": rol["id"], "nombre": rol["nombre"], "descripcion": rol.get("descripcion")}
        for rol in repo.obtener_todos()
    ]
