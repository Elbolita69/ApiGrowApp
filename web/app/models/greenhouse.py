from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GreenhouseBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    area_metros_cuadrados: Optional[float] = None
    capacidad_maxima: Optional[int] = None
    estado: str = "activo"

class GreenhouseCreate(GreenhouseBase):
    pass

class GreenhouseUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    area_metros_cuadrados: Optional[float] = None
    capacidad_maxima: Optional[int] = None
    estado: Optional[str] = None

class Greenhouse(GreenhouseBase):
    id: int
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True
