from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_permission
from app.models.sensor_reading import SensorReading, SensorReadingCreate, SensorReadingUpdate
from app.repositories.sensor_reading_repo import SensorReadingRepository

router = APIRouter(prefix="/sensor-readings", tags=["Lecturas de Sensores"])
repo = SensorReadingRepository()

@router.get("/", dependencies=[Depends(require_permission("sensor_readings", "ver"))])
async def listar_readings():
    return await repo.obtener_todos()

@router.get("/{reading_id}", dependencies=[Depends(require_permission("sensor_readings", "ver"))])
async def obtener_reading(reading_id: int):
    reading = await repo.obtener_por_id(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading

@router.get("/sensor/{sensor_id}", dependencies=[Depends(require_permission("sensor_readings", "ver"))])
async def listar_readings_por_sensor(sensor_id: int, limit: int = 50):
    return await repo.obtener_por_sensor(sensor_id, limit)

@router.get("/greenhouse/{greenhouse_id}/latest", dependencies=[Depends(require_permission("sensor_readings", "ver"))])
async def obtener_ultimas_lecturas(greenhouse_id: int, limit: int = 20):
    return await repo.obtener_ultimas_lecturas(greenhouse_id, limit)

@router.post("/", dependencies=[Depends(require_permission("sensor_readings", "crear"))])
async def crear_reading(reading: SensorReadingCreate):
    nuevo_id = await repo.crear(reading)
    return {"mensaje": "Lectura registrada exitosamente", "id": nuevo_id}

@router.put("/{reading_id}", dependencies=[Depends(require_permission("sensor_readings", "editar"))])
async def actualizar_sensor_reading(reading_id: int, datos: SensorReadingUpdate):
    if not await repo.actualizar(reading_id, datos):
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return {"mensaje": "Registro actualizado correctamente"}

@router.delete("/{reading_id}", dependencies=[Depends(require_permission("sensor_readings", "eliminar"))])
async def eliminar_sensor_reading(reading_id: int):
    if not await repo.eliminar(reading_id):
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return {"mensaje": "Registro eliminado correctamente"}
