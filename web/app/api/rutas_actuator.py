from fastapi import APIRouter, HTTPException
from app.models.actuator import Actuator, ActuatorCreate, ActuatorUpdate
from app.repositories.actuator_repo import ActuatorRepository

router = APIRouter(prefix="/actuators", tags=["Actuadores"])
repo = ActuatorRepository()

@router.get("/")
async def listar_actuators():
    return await repo.obtener_todos()

@router.get("/{actuator_id}")
async def obtener_actuator(actuator_id: int):
    actuator = await repo.obtener_por_id(actuator_id)
    if not actuator:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return actuator

@router.get("/greenhouse/{greenhouse_id}")
async def listar_actuators_por_greenhouse(greenhouse_id: int):
    return await repo.obtener_por_greenhouse(greenhouse_id)

@router.post("/")
async def crear_actuator(actuator: ActuatorCreate):
    nuevo_id = await repo.crear(actuator)
    return {"mensaje": "Actuador registrado exitosamente", "id": nuevo_id}

@router.put("/{actuator_id}")
async def actualizar_actuator(actuator_id: int, actuator: ActuatorUpdate):
    exito = await repo.actualizar(actuator_id, actuator)
    if not exito:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return {"mensaje": "Actuador actualizado correctamente"}

@router.delete("/{actuator_id}")
async def eliminar_actuator(actuator_id: int):
    exito = await repo.eliminar(actuator_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Actuador no encontrado")
    return {"mensaje": "Actuador eliminado correctamente"}
