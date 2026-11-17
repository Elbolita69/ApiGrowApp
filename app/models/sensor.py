from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    greenhouse_id: int
    tipo: str
    nombre: str
    unidad: str
    ubicacion: Optional[str] = None
    estado: bool = True


class SensorCreate(SensorBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class SensorUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    greenhouse_id: Optional[int] = None
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    unidad: Optional[str] = None
    ubicacion: Optional[str] = None


class Sensor(SensorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
