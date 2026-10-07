from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActuatorBase(BaseModel):
    greenhouse_id: int
    tipo: str
    nombre: str
    ubicacion: Optional[str] = None
    estado: bool = True

class ActuatorCreate(ActuatorBase):
    pass

class ActuatorUpdate(BaseModel):
    greenhouse_id: Optional[int] = None
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    estado: Optional[bool] = None

class Actuator(ActuatorBase):
    id: int
    fecha_instalacion: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
