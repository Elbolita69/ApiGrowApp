import os
from datetime import datetime, timedelta
from typing import Optional
import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-en-produccion-usar-variable-SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token. Returns None if invalid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """FastAPI dependency to get the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    return {"user_id": user_id, **payload}


def verify_rol(required_rol: str):
    """Returns a FastAPI dependency that checks if the user has the required rol."""

    def rol_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_rol = current_user.get("rol")
        if user_rol != required_rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol '{required_rol}' is required for this operation",
            )
        return current_user

    return rol_checker


_ACCIONES = {"ver": "puede_ver", "crear": "puede_crear", "editar": "puede_editar", "eliminar": "puede_eliminar"}


_db = None


def _get_db():
    """Una sola instancia (y un solo pool de conexiones) para validar permisos."""
    global _db
    if _db is None:
        from app.core.database import Database  # import local para evitar ciclos
        _db = Database()
    return _db


def require_permission(modulo: str, accion: str):
    """Dependencia FastAPI: valida el JWT y comprueba en la tabla moduloxrol
    que el rol del usuario tenga permiso (ver/crear/editar/eliminar) sobre el modulo."""
    columna = _ACCIONES[accion]

    async def checker(current_user: dict = Depends(get_current_user)) -> dict:
        db = _get_db()
        conn = await db.get_connection()
        try:
            permitido = await conn.fetchval(
                f"SELECT mr.{columna} FROM moduloxrol mr "
                "JOIN rol r ON r.id = mr.rol_id "
                "JOIN modulo m ON m.id = mr.modulo_id "
                "WHERE r.nombre = $1 AND m.nombre = $2 "
                "AND mr.estado = TRUE AND r.estado = TRUE AND m.estado = TRUE;",
                current_user.get("rol"),
                modulo,
            )
        finally:
            await db.release_connection(conn)
        if not permitido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El rol '{current_user.get('rol')}' no tiene permiso para {accion} en '{modulo}'",
            )
        return current_user

    return checker
