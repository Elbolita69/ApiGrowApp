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
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol_id: Optional[int] = None
    password: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
