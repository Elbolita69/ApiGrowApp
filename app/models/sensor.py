from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorBase(BaseModel):
    greenhouse_id: int
    tipo: str
    nombre: str
    unidad: str
    ubicacion: Optional[str] = None
    estado: bool = True

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    greenhouse_id: Optional[int] = None
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    unidad: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[bool] = None

class Sensor(SensorBase):
    id: int
    fecha_instalacion: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
