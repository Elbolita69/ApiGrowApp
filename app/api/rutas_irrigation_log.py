from fastapi import APIRouter, HTTPException
from app.models.irrigation_log import IrrigationLog, IrrigationLogCreate
from app.repositories.irrigation_log_repo import IrrigationLogRepository

router = APIRouter(prefix="/irrigation-logs", tags=["Historial de Riego"])
repo = IrrigationLogRepository()

@router.get("/")
async def listar_logs(limit: int = 100):
    return await repo.obtener_todos(limit)

@router.get("/{log_id}")
async def obtener_log(log_id: int):
    log = await repo.obtener_por_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Registro de riego no encontrado")
    return log

@router.get("/zone/{zone_id}")
async def listar_logs_por_zone(zone_id: int, limit: int = 50):
    return await repo.obtener_por_zone(zone_id, limit)

@router.post("/")
async def crear_log(log: IrrigationLogCreate):
    nuevo_id = await repo.crear(log)
    return {"mensaje": "Registro de riego creado exitosamente", "id": nuevo_id}
