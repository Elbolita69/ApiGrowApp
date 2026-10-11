from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActuatorControlBase(BaseModel):
    actuator_id: int
    usuario_id: Optional[int] = None
    accion: str
    valor_ajuste: Optional[str] = None
    resultado: str = "exitoso"

class ActuatorControlCreate(ActuatorControlBase):
    pass

class ActuatorControl(ActuatorControlBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
