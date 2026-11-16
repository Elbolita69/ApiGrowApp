from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActuatorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    greenhouse_id: int
    tipo: str
    nombre: str
    ubicacion: Optional[str] = None
    estado_actuador: str = "inactivo"
    estado: bool = True


class ActuatorCreate(ActuatorBase):
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ActuatorUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    greenhouse_id: Optional[int] = None
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    estado_actuador: Optional[str] = None


class Actuator(ActuatorBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_instalacion: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
