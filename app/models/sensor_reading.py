from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorReadingBase(BaseModel):
    sensor_id: int
    valor: float
    estado: bool = True

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingUpdate(BaseModel):
    sensor_id: Optional[int] = None
    valor: Optional[float] = None
    estado: Optional[bool] = None

class SensorReading(SensorReadingBase):
    id: int
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
