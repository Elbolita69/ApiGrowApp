from __future__ import annotations

import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

_secreto = os.getenv("SECRET_KEY")
if not _secreto:
    _secreto = secrets.token_urlsafe(48)
    logger.warning(
        "SECRET_KEY no esta definido en el entorno: se genero una clave aleatoria "
        "en memoria. Los tokens emitidos en este proceso dejaran de ser validos "
        "al reiniciar la aplicacion."
    )
SECRET_KEY = _secreto

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_ACCIONES = {
    "ver": "puede_ver",
    "crear": "puede_crear",
    "editar": "puede_editar",
    "eliminar": "puede_eliminar",
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    contenido = data.copy()
    if expires_delta:
        expira = datetime.now(timezone.utc) + expires_delta
    else:
        expira = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    contenido.update({"exp": expira})
    return jwt.encode(contenido, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credenciales_invalidas
    if payload.get("sub") is None:
        raise credenciales_invalidas
    return {"user_id": payload["sub"], **payload}


def get_current_user_id(current_user: dict = Depends(get_current_user)) -> int:
    try:
        return int(current_user["sub"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_rol(required_rol: str):
    def rol_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("rol") != required_rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El rol '{required_rol}' es obligatorio para esta operacion",
            )
        return current_user

    return rol_checker


_db = None


def _get_db():
    global _db
    if _db is None:
        from app.core.database import Database

        _db = Database()
    return _db


def require_permission(modulo: str, accion: str):
    columna = _ACCIONES[accion]
    sql = (
        f"SELECT mr.{columna} AS permitido "
        "FROM moduloxrol mr "
        "JOIN rol r ON r.id = mr.rol_id "
        "JOIN modulo m ON m.id = mr.modulo_id "
        "WHERE r.nombre = %s AND m.nombre = %s "
        "AND mr.estado = TRUE AND r.estado = TRUE AND m.estado = TRUE;"
    )

    def checker(current_user: dict = Depends(get_current_user)) -> dict:
        rol = current_user.get("rol")
        db = _get_db()
        with db.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (rol, modulo))
                fila = cur.fetchone()
        permitido = bool(fila and fila.get("permitido"))
        if not permitido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"El rol '{rol}' no tiene permiso para {accion} en '{modulo}'"
                ),
            )
        return current_user

    return checker
