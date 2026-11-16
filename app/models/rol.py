from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RolBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True


class RolCreate(RolBase):
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class RolUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class Rol(RolBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
