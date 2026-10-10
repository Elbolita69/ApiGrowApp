from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nombre: Optional[str] = None
    rol_id: Optional[int] = None
    estado: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol_id: Optional[int] = None
    estado: Optional[bool] = None

class User(UserBase):
    id: int
    password_hash: str
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
