from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    greenhouse_id: int
    sensor_id: Optional[int] = None
    tipo: str
    mensaje: str
    valor_actual: Optional[float] = None
    umbral: Optional[float] = None
    prioridad: str = "media"
    estado: bool = True

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    greenhouse_id: Optional[int] = None
    sensor_id: Optional[int] = None
    tipo: Optional[str] = None
    mensaje: Optional[str] = None
    valor_actual: Optional[float] = None
    umbral: Optional[float] = None
    prioridad: Optional[str] = None
    estado: Optional[bool] = None

class Alert(AlertBase):
    id: int
    timestamp: Optional[datetime] = None
    resuelta_en: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
