from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CropBatchBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: Optional[int] = None
    greenhouse_id: int
    fecha_siembra: date
    fecha_cosecha_estimada: Optional[date] = None
    fecha_cosecha_real: Optional[date] = None
    cantidad_plantas: Optional[int] = None
    estado_cultivo: Optional[str] = "creciendo"
    notas: Optional[str] = None
    estado: bool = True


class CropBatchCreate(CropBatchBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class CropBatchUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    crop_id: Optional[int] = None
    greenhouse_id: Optional[int] = None
    fecha_siembra: Optional[date] = None
    fecha_cosecha_estimada: Optional[date] = None
    fecha_cosecha_real: Optional[date] = None
    cantidad_plantas: Optional[int] = None
    estado_cultivo: Optional[str] = None
    notas: Optional[str] = None


class CropBatch(CropBatchBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
