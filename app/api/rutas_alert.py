from fastapi import APIRouter, HTTPException
from app.models.alert import Alert, AlertCreate, AlertUpdate
from app.repositories.alert_repo import AlertRepository

router = APIRouter(prefix="/alerts", tags=["Alertas"])
repo = AlertRepository()

@router.get("/")
async def listar_alerts():
    return await repo.obtener_todos()

@router.get("/activas")
async def listar_alerts_activas():
    return await repo.obtener_activas()

@router.get("/{alert_id}")
async def obtener_alert(alert_id: int):
    alert = await repo.obtener_por_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alert

@router.post("/")
async def crear_alert(alert: AlertCreate):
    nuevo_id = await repo.crear(alert)
    return {"mensaje": "Alerta registrada exitosamente", "id": nuevo_id}

@router.patch("/{alert_id}/resolver")
async def resolver_alert(alert_id: int):
    exito = await repo.actualizar_estado(alert_id, "resuelta")
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta resuelta correctamente"}

@router.patch("/{alert_id}/reconocer")
async def reconocer_alert(alert_id: int):
    exito = await repo.actualizar_estado(alert_id, "reconocida")
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta reconocida correctamente"}
