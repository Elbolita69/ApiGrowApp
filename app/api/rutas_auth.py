from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from app.models.user import UserCreate
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["Autenticacion"])
repo = UserRepository()

ROL_POR_DEFECTO = "lector"


class Token(BaseModel):
    access_token: str
    token_type: str


class RegistroUsuario(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: EmailStr
    password: str
    nombre: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nombre: Optional[str] = None
    rol: Optional[str] = None


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = repo.obtener_credenciales_por_username(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.get("estado"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.get("password_hash") or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    rol_nombre = user.get("rol_nombre") or ROL_POR_DEFECTO
    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "username": user["username"],
            "rol": rol_nombre,
        },
        expires_delta=timedelta(hours=24),
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: RegistroUsuario):
    if repo.obtener_por_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya esta registrado",
        )

    rol = repo.obtener_por_rol(ROL_POR_DEFECTO)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"El rol '{ROL_POR_DEFECTO}' no esta configurado en la base de datos",
        )

    nuevo_id = repo.crear(
        UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            nombre=user_data.nombre,
            rol_id=rol["id"],
        )
    )

    return UserResponse(
        id=nuevo_id,
        username=user_data.username,
        email=user_data.email,
        nombre=user_data.nombre,
        rol=ROL_POR_DEFECTO,
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    user = repo.obtener_por_id(int(current_user["sub"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        nombre=user.get("nombre"),
        rol=user.get("rol_nombre") or current_user.get("rol"),
    )


@router.get("/modulos")
def modulos_del_rol(current_user: dict = Depends(get_current_user)):
    db = repo.db
    with db.get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT m.nombre, m.descripcion, mr.puede_ver, mr.puede_crear, "
                "mr.puede_editar, mr.puede_eliminar "
                "FROM moduloxrol mr "
                "JOIN rol r ON r.id = mr.rol_id "
                "JOIN modulo m ON m.id = mr.modulo_id "
                "WHERE r.nombre = %s AND mr.estado = TRUE AND r.estado = TRUE "
                "AND m.estado = TRUE AND mr.puede_ver = TRUE ORDER BY m.id;",
                (current_user.get("rol"),),
            )
            filas = cur.fetchall()

    return [dict(fila) for fila in filas]
