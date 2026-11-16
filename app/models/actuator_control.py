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
    """Datos de entrada: sin `id`.

    `usuario_id` NO se toma del cuerpo de la peticion: el backend lo inyecta
    con el usuario autenticado. El campo se conserva unicamente para tolerar
    clientes que lo envian (se ignora).
    """

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    usuario_id: Optional[int] = None


class ActuatorControlUpdate(BaseModel):
    """Actualizacion parcial: sin `id` ni campos primary key editables."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    actuator_id: Optional[int] = None
    accion: Optional[str] = None
    valor_ajuste: Optional[str] = None
    resultado: Optional[str] = None


class ActuatorControl(ActuatorControlBase):
    """Modelo de lectura: incluye la auditoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
