from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorReadingBase(BaseModel):
    sensor_id: int
    valor: float

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReading(SensorReadingBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
