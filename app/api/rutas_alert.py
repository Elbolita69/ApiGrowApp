from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.alert import AlertCreate, AlertUpdate
from app.repositories.alert_repo import AlertRepository

router = APIRouter(prefix="/alerts", tags=["Alertas"])
repo = AlertRepository()


@router.get("/", dependencies=[Depends(require_permission("alerts", "ver"))])
def listar_alerts():
    return repo.obtener_todos()


@router.get("/activas", dependencies=[Depends(require_permission("alerts", "ver"))])
def listar_alerts_activas():
    return repo.obtener_activas()


@router.get("/{alert_id}", dependencies=[Depends(require_permission("alerts", "ver"))])
def obtener_alert(alert_id: int):
    alert = repo.obtener_por_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alert


@router.post("/", dependencies=[Depends(require_permission("alerts", "crear"))])
def crear_alert(alert: AlertCreate):
    nuevo_id = repo.crear(alert)
    return {"mensaje": "Alerta registrada exitosamente", "id": nuevo_id}


@router.patch(
    "/{alert_id}/resolver", dependencies=[Depends(require_permission("alerts", "editar"))]
)
def resolver_alert(alert_id: int):
    exito = repo.actualizar_estado(alert_id, "resuelta")
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta resuelta correctamente"}


@router.patch(
    "/{alert_id}/reconocer",
    dependencies=[Depends(require_permission("alerts", "editar"))],
)
def reconocer_alert(alert_id: int):
    exito = repo.actualizar_estado(alert_id, "reconocida")
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta reconocida correctamente"}


@router.put("/{alert_id}", dependencies=[Depends(require_permission("alerts", "editar"))])
def actualizar_alert(alert_id: int, datos: AlertUpdate):
    if not repo.actualizar(alert_id, datos):
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Registro actualizado correctamente"}


@router.delete(
    "/{alert_id}", dependencies=[Depends(require_permission("alerts", "eliminar"))]
)
def eliminar_alert(alert_id: int):
    if not repo.eliminar(alert_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Registro eliminado correctamente"}
