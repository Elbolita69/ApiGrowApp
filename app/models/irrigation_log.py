from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IrrigationLogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    zone_id: int
    duracion_minutos: int
    cantidad_agua_litros: Optional[float] = None
    modo: str = "automatico"
    resultado: str = "exitoso"
    notas: Optional[str] = None
    estado: bool = True


class IrrigationLogCreate(IrrigationLogBase):
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class IrrigationLogUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    zone_id: Optional[int] = None
    duracion_minutos: Optional[int] = None
    cantidad_agua_litros: Optional[float] = None
    modo: Optional[str] = None
    resultado: Optional[str] = None
    notas: Optional[str] = None


class IrrigationLog(IrrigationLogBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
