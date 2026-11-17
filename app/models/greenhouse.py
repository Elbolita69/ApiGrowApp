from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GreenhouseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombre: str
    ubicacion: Optional[str] = None
    area_metros_cuadrados: Optional[float] = None
    capacidad_maxima: Optional[int] = None
    estado: bool = True


class GreenhouseCreate(GreenhouseBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class GreenhouseUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    area_metros_cuadrados: Optional[float] = None
    capacidad_maxima: Optional[int] = None


class Greenhouse(GreenhouseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
