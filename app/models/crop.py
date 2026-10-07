from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CropBase(BaseModel):
    nombre: str
    nombre_cientifico: Optional[str] = None
    temperatura_min: Optional[float] = None
    temperatura_max: Optional[float] = None
    humedad_min: Optional[float] = None
    humedad_max: Optional[float] = None
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    ciclo_dias: Optional[int] = None
    descripcion: Optional[str] = None
    estado: bool = True

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_cientifico: Optional[str] = None
    temperatura_min: Optional[float] = None
    temperatura_max: Optional[float] = None
    humedad_min: Optional[float] = None
    humedad_max: Optional[float] = None
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    ciclo_dias: Optional[int] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None

class Crop(CropBase):
    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
