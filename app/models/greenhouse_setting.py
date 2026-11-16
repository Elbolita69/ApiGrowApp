from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GreenhouseSettingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    greenhouse_id: int
    temp_min: float = 15.00
    temp_max: float = 30.00
    humedad_min: float = 40.00
    humedad_max: float = 80.00
    luz_min: float = 100.00
    ph_min: float = 5.50
    ph_max: float = 7.00
    intervalo_lectura_minutos: int = 15
    estado: bool = True


class GreenhouseSettingCreate(GreenhouseSettingBase):
    """Datos de entrada: sin `id` (lo asigna la base de datos)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class GreenhouseSettingUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    humedad_min: Optional[float] = None
    humedad_max: Optional[float] = None
    luz_min: Optional[float] = None
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    intervalo_lectura_minutos: Optional[int] = None


class GreenhouseSetting(GreenhouseSettingBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    actualizado_en: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
