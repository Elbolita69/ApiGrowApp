from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActuatorControlBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actuator_id: int
    accion: str
    valor_ajuste: Optional[str] = None
    resultado: str = "exitoso"
    estado: bool = True


class ActuatorControlCreate(ActuatorControlBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    usuario_id: Optional[int] = None


class ActuatorControlUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    actuator_id: Optional[int] = None
    accion: Optional[str] = None
    valor_ajuste: Optional[str] = None
    resultado: Optional[str] = None


class ActuatorControl(ActuatorControlBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
