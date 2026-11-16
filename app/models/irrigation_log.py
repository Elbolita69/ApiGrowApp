from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IrrigationLogBase(BaseModel):
    zone_id: int
    duracion_minutos: int
    cantidad_agua_litros: Optional[float] = None
    modo: str = "automatico"
    resultado: str = "exitoso"
    notas: Optional[str] = None
    estado: bool = True

class IrrigationLogCreate(IrrigationLogBase):
    pass

class IrrigationLogUpdate(BaseModel):
    zone_id: Optional[int] = None
    duracion_minutos: Optional[int] = None
    cantidad_agua_litros: Optional[float] = None
    modo: Optional[str] = None
    resultado: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[bool] = None

class IrrigationLog(IrrigationLogBase):
    id: int
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
