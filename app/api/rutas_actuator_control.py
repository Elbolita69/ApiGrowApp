from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user_id, require_permission
from app.models.actuator_control import ActuatorControlCreate, ActuatorControlUpdate
from app.repositories.actuator_control_repo import ActuatorControlRepository

router = APIRouter(prefix="/actuator-controls", tags=["Control de Actuadores"])
repo = ActuatorControlRepository()


@router.get("/", dependencies=[Depends(require_permission("actuator_controls", "ver"))])
def listar_controls(limit: int = 100):
    return repo.obtener_todos(limit)


@router.get(
    "/{control_id}", dependencies=[Depends(require_permission("actuator_controls", "ver"))]
)
def obtener_control(control_id: int):
    control = repo.obtener_por_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return control


@router.get(
    "/actuator/{actuator_id}",
    dependencies=[Depends(require_permission("actuator_controls", "ver"))],
)
def listar_controls_por_actuator(actuator_id: int, limit: int = 50):
    return repo.obtener_por_actuator(actuator_id, limit)


@router.post("/", dependencies=[Depends(require_permission("actuator_controls", "crear"))])
def crear_control(
    control: ActuatorControlCreate,
    usuario_id: int = Depends(get_current_user_id),
):
    """Registra una orden de control.

    `usuario_id` lo inyecta el backend con el usuario autenticado: nunca se
    toma del cuerpo de la peticion.
    """
    nuevo_id = repo.crear(control, usuario_id=usuario_id)
    return {"mensaje": "Control registrado exitosamente", "id": nuevo_id}


@router.put(
    "/{control_id}", dependencies=[Depends(require_permission("actuator_controls", "editar"))]
)
def actualizar_actuator_control(control_id: int, datos: ActuatorControlUpdate):
    if not repo.actualizar(control_id, datos):
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return {"mensaje": "Registro actualizado correctamente"}


@router.delete(
    "/{control_id}",
    dependencies=[Depends(require_permission("actuator_controls", "eliminar"))],
)
def eliminar_actuator_control(control_id: int):
    if not repo.eliminar(control_id):
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return {"mensaje": "Registro eliminado correctamente"}
