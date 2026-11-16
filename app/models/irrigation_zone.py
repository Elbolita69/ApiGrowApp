from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IrrigationZoneBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    greenhouse_id: int
    nombre: str
    capacidad_litros_min: Optional[float] = None
    capacidad_litros_max: Optional[float] = None
    tipo: str = "gotas"
    estado: bool = True


class IrrigationZoneCreate(IrrigationZoneBase):
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class IrrigationZoneUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    greenhouse_id: Optional[int] = None
    nombre: Optional[str] = None
    capacidad_litros_min: Optional[float] = None
    capacidad_litros_max: Optional[float] = None
    tipo: Optional[str] = None


class IrrigationZone(IrrigationZoneBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
