from fastapi import APIRouter, HTTPException
from app.models.actuator_control import ActuatorControl, ActuatorControlCreate
from app.repositories.actuator_control_repo import ActuatorControlRepository

router = APIRouter(prefix="/actuator-controls", tags=["Control de Actuadores"])
repo = ActuatorControlRepository()

@router.get("/")
async def listar_controls(limit: int = 100):
    return await repo.obtener_todos(limit)

@router.get("/{control_id}")
async def obtener_control(control_id: int):
    control = await repo.obtener_por_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return control

@router.get("/actuator/{actuator_id}")
async def listar_controls_por_actuator(actuator_id: int, limit: int = 50):
    return await repo.obtener_por_actuator(actuator_id, limit)

@router.post("/")
async def crear_control(control: ActuatorControlCreate):
    nuevo_id = await repo.crear(control)
    return {"mensaje": "Control registrado exitosamente", "id": nuevo_id}
