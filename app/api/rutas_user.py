from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User, UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository
from app.core.auth import get_current_user, verify_rol

router = APIRouter(prefix="/users", tags=["Usuarios"])
repo = UserRepository()

@router.get("/")
async def listar_users(_: dict = Depends(get_current_user)):
    return await repo.obtener_todos()

@router.get("/{user_id}")
async def obtener_user(user_id: int, _: dict = Depends(get_current_user)):
    user = await repo.obtener_por_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/username/{username}")
async def obtener_user_por_username(username: str, _: dict = Depends(get_current_user)):
    user = await repo.obtener_por_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/")
async def crear_user(user: UserCreate, _: dict = Depends(verify_rol("administrador")):
    nuevo_id = await repo.crear(user)
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.put("/{user_id}")
async def actualizar_user(user_id: int, user: UserUpdate, _: dict = Depends(verify_rol("administrador")):
    exito = await repo.actualizar(user_id, user)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/{user_id}")
async def eliminar_user(user_id: int, _: dict = Depends(verify_rol("administrador")):
    exito = await repo.eliminar(user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
