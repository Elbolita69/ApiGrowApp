from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_permission
from app.models.actuator_control import ActuatorControl, ActuatorControlCreate, ActuatorControlUpdate
from app.repositories.actuator_control_repo import ActuatorControlRepository

router = APIRouter(prefix="/actuator-controls", tags=["Control de Actuadores"])
repo = ActuatorControlRepository()

@router.get("/", dependencies=[Depends(require_permission("actuator_controls", "ver"))])
async def listar_controls(limit: int = 100):
    return await repo.obtener_todos(limit)

@router.get("/{control_id}", dependencies=[Depends(require_permission("actuator_controls", "ver"))])
async def obtener_control(control_id: int):
    control = await repo.obtener_por_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return control

@router.get("/actuator/{actuator_id}", dependencies=[Depends(require_permission("actuator_controls", "ver"))])
async def listar_controls_por_actuator(actuator_id: int, limit: int = 50):
    return await repo.obtener_por_actuator(actuator_id, limit)

@router.post("/", dependencies=[Depends(require_permission("actuator_controls", "crear"))])
async def crear_control(control: ActuatorControlCreate):
    nuevo_id = await repo.crear(control)
    return {"mensaje": "Control registrado exitosamente", "id": nuevo_id}

@router.put("/{control_id}", dependencies=[Depends(require_permission("actuator_controls", "editar"))])
async def actualizar_actuator_control(control_id: int, datos: ActuatorControlUpdate):
    if not await repo.actualizar(control_id, datos):
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return {"mensaje": "Registro actualizado correctamente"}

@router.delete("/{control_id}", dependencies=[Depends(require_permission("actuator_controls", "eliminar"))])
async def eliminar_actuator_control(control_id: int):
    if not await repo.eliminar(control_id):
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return {"mensaje": "Registro eliminado correctamente"}
