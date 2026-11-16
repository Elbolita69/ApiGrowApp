from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CropBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class CropUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

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


class Crop(CropBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
