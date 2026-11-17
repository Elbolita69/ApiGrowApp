from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SensorReadingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sensor_id: int
    valor: float
    estado: bool = True


class SensorReadingCreate(SensorReadingBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class SensorReadingUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    sensor_id: Optional[int] = None
    valor: Optional[float] = None


class SensorReading(SensorReadingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
