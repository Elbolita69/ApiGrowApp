from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_permission
from app.models.user import User, UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/users", tags=["Usuarios"])
repo = UserRepository()

@router.get("/", dependencies=[Depends(require_permission("usuario", "ver"))])
async def listar_users():
    return await repo.obtener_todos()

@router.get("/{user_id}", dependencies=[Depends(require_permission("usuario", "ver"))])
async def obtener_user(user_id: int):
    user = await repo.obtener_por_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/username/{username}", dependencies=[Depends(require_permission("usuario", "ver"))])
async def obtener_user_por_username(username: str):
    user = await repo.obtener_por_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", dependencies=[Depends(require_permission("usuario", "crear"))])
async def crear_user(user: UserCreate):
    nuevo_id = await repo.crear(user)
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.put("/{user_id}", dependencies=[Depends(require_permission("usuario", "editar"))])
async def actualizar_user(user_id: int, user: UserUpdate):
    exito = await repo.actualizar(user_id, user)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/{user_id}", dependencies=[Depends(require_permission("usuario", "eliminar"))])
async def eliminar_user(user_id: int):
    exito = await repo.eliminar(user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
