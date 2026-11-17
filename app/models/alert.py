from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    greenhouse_id: int
    sensor_id: Optional[int] = None
    tipo: str
    mensaje: str
    valor_actual: Optional[float] = None
    umbral: Optional[float] = None
    prioridad: str = "media"
    estado_alerta: str = "activa"
    estado: bool = True


class AlertCreate(AlertBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class AlertUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    greenhouse_id: Optional[int] = None
    sensor_id: Optional[int] = None
    tipo: Optional[str] = None
    mensaje: Optional[str] = None
    valor_actual: Optional[float] = None
    umbral: Optional[float] = None
    prioridad: Optional[str] = None
    estado_alerta: Optional[str] = None


class Alert(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: Optional[datetime] = None
    resuelta_en: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
