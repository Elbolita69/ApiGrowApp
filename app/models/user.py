from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nombre: Optional[str] = None
    rol: str = "operador"
    estado: str = "activo"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None

class User(UserBase):
    id: int
    password_hash: str
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True
