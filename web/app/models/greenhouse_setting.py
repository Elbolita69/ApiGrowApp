from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GreenhouseSettingBase(BaseModel):
    greenhouse_id: int
    temp_min: float = 15.00
    temp_max: float = 30.00
    humedad_min: float = 40.00
    humedad_max: float = 80.00
    luz_min: float = 100.00
    ph_min: float = 5.50
    ph_max: float = 7.00
    intervalo_lectura_minutos: int = 15

class GreenhouseSettingCreate(GreenhouseSettingBase):
    pass

class GreenhouseSettingUpdate(BaseModel):
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    humedad_min: Optional[float] = None
    humedad_max: Optional[float] = None
    luz_min: Optional[float] = None
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    intervalo_lectura_minutos: Optional[int] = None

class GreenhouseSetting(GreenhouseSettingBase):
    id: int
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
