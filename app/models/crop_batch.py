from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CropBatchBase(BaseModel):
    crop_id: Optional[int] = None
    greenhouse_id: int
    fecha_siembra: date
    fecha_cosecha_estimada: Optional[date] = None
    fecha_cosecha_real: Optional[date] = None
    cantidad_plantas: Optional[int] = None
    estado: bool = True
    notas: Optional[str] = None

class CropBatchCreate(CropBatchBase):
    pass

class CropBatchUpdate(BaseModel):
    crop_id: Optional[int] = None
    greenhouse_id: Optional[int] = None
    fecha_siembra: Optional[date] = None
    fecha_cosecha_estimada: Optional[date] = None
    fecha_cosecha_real: Optional[date] = None
    cantidad_plantas: Optional[int] = None
    estado: Optional[bool] = None
    notas: Optional[str] = None

class CropBatch(CropBatchBase):
    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
