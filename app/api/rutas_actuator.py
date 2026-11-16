from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.actuator import ActuatorCreate, ActuatorUpdate
from app.repositories.actuator_repo import ActuatorRepository

router = APIRouter(prefix="/actuators", tags=["Actuadores"])
repo = ActuatorRepository()


@router.get("/", dependencies=[Depends(require_permission("actuators", "ver"))])
def listar_actuators():
    return repo.obtener_todos()


@router.get(
    "/{actuator_id}", dependencies=[Depends(require_permission("actuators", "ver"))]
)
def obtener_actuator(actuator_id: int):
    actuator = repo.obtener_por_id(actuator_id)
    if not actuator:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return actuator


@router.get(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("actuators", "ver"))],
)
def listar_actuators_por_greenhouse(greenhouse_id: int):
    return repo.obtener_por_greenhouse(greenhouse_id)


@router.post("/", dependencies=[Depends(require_permission("actuators", "crear"))])
def crear_actuator(actuator: ActuatorCreate):
    nuevo_id = repo.crear(actuator)
    return {"mensaje": "Actuador registrado exitosamente", "id": nuevo_id}


@router.put(
    "/{actuator_id}", dependencies=[Depends(require_permission("actuators", "editar"))]
)
def actualizar_actuator(actuator_id: int, actuator: ActuatorUpdate):
    exito = repo.actualizar(actuator_id, actuator)
    if not exito:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return {"mensaje": "Actuador actualizado correctamente"}


@router.delete(
    "/{actuator_id}",
    dependencies=[Depends(require_permission("actuators", "eliminar"))],
)
def eliminar_actuator(actuator_id: int):
    exito = repo.eliminar(actuator_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return {"mensaje": "Actuador eliminado correctamente"}
