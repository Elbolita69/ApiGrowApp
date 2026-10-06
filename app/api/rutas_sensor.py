from fastapi import APIRouter, HTTPException
from app.models.sensor import Sensor, SensorCreate, SensorUpdate
from app.repositories.sensor_repo import SensorRepository

router = APIRouter(prefix="/sensors", tags=["Sensores"])
repo = SensorRepository()

@router.get("/")
async def listar_sensors():
    return await repo.obtener_todos()

@router.get("/{sensor_id}")
async def obtener_sensor(sensor_id: int):
    sensor = await repo.obtener_por_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.get("/greenhouse/{greenhouse_id}")
async def listar_sensors_por_greenhouse(greenhouse_id: int):
    return await repo.obtener_por_greenhouse(greenhouse_id)

@router.post("/")
async def crear_sensor(sensor: SensorCreate):
    nuevo_id = await repo.crear(sensor)
    return {"mensaje": "Sensor registrado exitosamente", "id": nuevo_id}

@router.put("/{sensor_id}")
async def actualizar_sensor(sensor_id: int, sensor: SensorUpdate):
    exito = await repo.actualizar(sensor_id, sensor)
    if not exito:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor actualizado correctamente"}

@router.delete("/{sensor_id}")
async def eliminar_sensor(sensor_id: int):
    exito = await repo.eliminar(sensor_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor eliminado correctamente"}
