from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    nombre: Optional[str] = None
    rol_id: Optional[int] = None
    estado: bool = True


class UserCreate(UserBase):
    """Datos de entrada: sin `id` y sin `password_hash` (lo genera el backend)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    password: str


class UserUpdate(BaseModel):
    """Actualizacion parcial: sin `id`.

    `rol_id` solo lo puede cambiar un administrador (se valida en el router).
    """

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol_id: Optional[int] = None
    password: Optional[str] = None


class User(UserBase):
    """Modelo de lectura: incluye la auditoria y nunca expone el hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
