from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EstudianteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombre: str
    grado: int
    promedio: float = Field(ge=0, le=5)
    estado: bool = True


class EstudianteCreate(EstudianteBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class EstudianteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    nombre: Optional[str] = None
    grado: Optional[int] = None
    promedio: Optional[float] = Field(default=None, ge=0, le=5)


class Estudiante(EstudianteBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class EstudianteResponse(EstudianteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado: Optional[datetime] = None
    actualizado: Optional[datetime] = None
