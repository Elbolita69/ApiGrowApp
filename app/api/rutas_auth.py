from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from app.core.database import Database

router = APIRouter(prefix="/auth", tags=["Autenticacion"])
db = Database()


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    nombre: str
    rol_id: int = 2


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nombre: str
    rol_id: int


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Autentica un usuario y retorna un token JWT."""
    conn = await db.get_connection()
    try:
        user = await conn.fetchrow(
            "SELECT id, username, password_hash, rol_id, estado "
            "FROM usuario WHERE username = $1",
            form_data.username,
        )
    finally:
        await db.release_connection(conn)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["estado"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    conn2 = await db.get_connection()
    try:
        rol_row = await conn2.fetchrow(
            "SELECT nombre FROM rol WHERE id = $1",
            user["rol_id"],
        )
        rol_nombre = rol_row["nombre"] if rol_row else "readonly"
    finally:
        await db.release_connection(conn2)

    access_token = create_access_token(
        data={
            "sub": str(user["id"]),
            "username": user["username"],
            "rol": rol_nombre,
        },
        expires_delta=timedelta(hours=24),
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Registra un nuevo usuario."""
    conn = await db.get_connection()
    try:
        existing = await conn.fetchrow(
            "SELECT id FROM usuario WHERE username = $1 OR email = $2",
            user_data.username,
            user_data.email,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username o email ya estan registrados",
            )

        password_hash = get_password_hash(user_data.password)

        row = await conn.fetchrow(
            "INSERT INTO usuario (username, email, password_hash, nombre, rol_id, estado) "
            "VALUES ($1, $2, $3, $4, $5, TRUE) "
            "RETURNING id, username, email, nombre, rol_id",
            user_data.username,
            user_data.email,
            password_hash,
            user_data.nombre,
            user_data.rol_id,
        )
    finally:
        await db.release_connection(conn)

    return UserResponse(**row)


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    """Retorna la informacion del usuario autenticado."""
    conn = await db.get_connection()
    try:
        user = await conn.fetchrow(
            "SELECT id, username, email, nombre, rol_id "
            "FROM usuario WHERE id = $1",
            int(current_user["sub"]),
        )
    finally:
        await db.release_connection(conn)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return UserResponse(**user)
