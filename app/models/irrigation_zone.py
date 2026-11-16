from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IrrigationZoneBase(BaseModel):
    greenhouse_id: int
    nombre: str
    capacidad_litros_min: Optional[float] = None
    capacidad_litros_max: Optional[float] = None
    tipo: str = "gotas"
    estado: bool = True

class IrrigationZoneCreate(IrrigationZoneBase):
    pass

class IrrigationZoneUpdate(BaseModel):
    greenhouse_id: Optional[int] = None
    nombre: Optional[str] = None
    capacidad_litros_min: Optional[float] = None
    capacidad_litros_max: Optional[float] = None
    tipo: Optional[str] = None
    estado: Optional[bool] = None

class IrrigationZone(IrrigationZoneBase):
    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
