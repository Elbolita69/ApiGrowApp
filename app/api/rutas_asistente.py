from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from app.core.asistente import (
    SqlNoPermitidoError,
    get_schema,
    responder_en_lenguaje_natural,
)
from app.core.auth import get_current_user

router = APIRouter(prefix="/asistente", tags=["Asistente"])


class Pregunta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pregunta: str


@router.post("/preguntar")
def preguntar(pregunta: Pregunta, current_user: dict = Depends(get_current_user)):
    """Responde una pregunta sobre la base de datos SOLO en lenguaje natural."""
    try:
        respuesta = responder_en_lenguaje_natural(pregunta.pregunta, current_user)
    except SqlNoPermitidoError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        )

    return {"respuesta": respuesta}


@router.get("/schema")
def esquema_de_la_base_de_datos(current_user: dict = Depends(get_current_user)):
    """Estructura de la base de datos (para depuracion)."""
    try:
        return get_schema()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo leer la estructura de la base de datos",
        )
