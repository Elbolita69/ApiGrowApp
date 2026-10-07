from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActuatorControlBase(BaseModel):
    actuator_id: int
    usuario_id: Optional[int] = None
    accion: str
    valor_ajuste: Optional[str] = None
    resultado: str = "exitoso"
    estado: bool = True

class ActuatorControlCreate(ActuatorControlBase):
    pass

class ActuatorControlUpdate(BaseModel):
    actuator_id: Optional[int] = None
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    valor_ajuste: Optional[str] = None
    resultado: Optional[str] = None
    estado: Optional[bool] = None

class ActuatorControl(ActuatorControlBase):
    id: int
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None

    class Config:
        from_attributes = True
