from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.irrigation_log import IrrigationLogCreate, IrrigationLogUpdate
from app.repositories.irrigation_log_repo import IrrigationLogRepository

router = APIRouter(prefix="/irrigation-logs", tags=["Historial de Riego"])
repo = IrrigationLogRepository()


@router.get("/", dependencies=[Depends(require_permission("irrigation_logs", "ver"))])
def listar_logs(limit: int = 100):
    return repo.obtener_todos(limit)


@router.get("/{log_id}", dependencies=[Depends(require_permission("irrigation_logs", "ver"))])
def obtener_log(log_id: int):
    log = repo.obtener_por_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Registro de riego no encontrado")
    return log


@router.get(
    "/zone/{zone_id}", dependencies=[Depends(require_permission("irrigation_logs", "ver"))]
)
def listar_logs_por_zone(zone_id: int, limit: int = 50):
    return repo.obtener_por_zone(zone_id, limit)


@router.post("/", dependencies=[Depends(require_permission("irrigation_logs", "crear"))])
def crear_log(log: IrrigationLogCreate):
    nuevo_id = repo.crear(log)
    return {"mensaje": "Registro de riego creado exitosamente", "id": nuevo_id}


@router.put(
    "/{log_id}", dependencies=[Depends(require_permission("irrigation_logs", "editar"))]
)
def actualizar_irrigation_log(log_id: int, datos: IrrigationLogUpdate):
    if not repo.actualizar(log_id, datos):
        raise HTTPException(status_code=404, detail="Registro de riego no encontrado")
    return {"mensaje": "Registro actualizado correctamente"}


@router.delete(
    "/{log_id}", dependencies=[Depends(require_permission("irrigation_logs", "eliminar"))]
)
def eliminar_irrigation_log(log_id: int):
    if not repo.eliminar(log_id):
        raise HTTPException(status_code=404, detail="Registro de riego no encontrado")
    return {"mensaje": "Registro eliminado correctamente"}
