from fastapi import APIRouter, HTTPException
from app.models.sensor_reading import SensorReading, SensorReadingCreate
from app.repositories.sensor_reading_repo import SensorReadingRepository

router = APIRouter(prefix="/sensor-readings", tags=["Lecturas de Sensores"])
repo = SensorReadingRepository()

@router.get("/")
async def listar_readings():
    return await repo.obtener_todos()

@router.get("/{reading_id}")
async def obtener_reading(reading_id: int):
    reading = await repo.obtener_por_id(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading

@router.get("/sensor/{sensor_id}")
async def listar_readings_por_sensor(sensor_id: int, limit: int = 50):
    return await repo.obtener_por_sensor(sensor_id, limit)

@router.get("/greenhouse/{greenhouse_id}/latest")
async def obtener_ultimas_lecturas(greenhouse_id: int, limit: int = 20):
    return await repo.obtener_ultimas_lecturas(greenhouse_id, limit)

@router.post("/")
async def crear_reading(reading: SensorReadingCreate):
    nuevo_id = await repo.crear(reading)
    return {"mensaje": "Lectura registrada exitosamente", "id": nuevo_id}
