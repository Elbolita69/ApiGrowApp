from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user, require_permission
from app.models.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/users", tags=["Usuarios"])
repo = UserRepository()

ROL_ADMINISTRADOR = "administrador"


@router.get("/", dependencies=[Depends(require_permission("usuario", "ver"))])
def listar_users():
    return repo.obtener_todos()


@router.get("/{user_id}", dependencies=[Depends(require_permission("usuario", "ver"))])
def obtener_user(user_id: int):
    user = repo.obtener_por_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.get(
    "/username/{username}", dependencies=[Depends(require_permission("usuario", "ver"))]
)
def obtener_user_por_username(username: str):
    user = repo.obtener_por_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/", dependencies=[Depends(require_permission("usuario", "crear"))])
def crear_user(user: UserCreate):
    nuevo_id = repo.crear(user)
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}


@router.put("/{user_id}", dependencies=[Depends(require_permission("usuario", "editar"))])
def actualizar_user(
    user_id: int,
    user: UserUpdate,
    current_user: dict = Depends(get_current_user),
):
    # Solo un administrador puede cambiar el rol de un usuario.
    if "rol_id" in user.model_fields_set and current_user.get("rol") != ROL_ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un administrador puede cambiar el rol de un usuario",
        )

    exito = repo.actualizar(user_id, user)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete(
    "/{user_id}", dependencies=[Depends(require_permission("usuario", "eliminar"))]
)
def eliminar_user(user_id: int, current_user: dict = Depends(get_current_user)):
    # Borrado logico (estado = FALSE) y solo para administradores.
    if current_user.get("rol") != ROL_ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un administrador puede eliminar usuarios",
        )

    exito = repo.eliminar(user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
