from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.irrigation_zone import IrrigationZoneCreate, IrrigationZoneUpdate
from app.repositories.irrigation_zone_repo import IrrigationZoneRepository

router = APIRouter(prefix="/irrigation-zones", tags=["Zonas de Riego"])
repo = IrrigationZoneRepository()


@router.get("/", dependencies=[Depends(require_permission("irrigation_zones", "ver"))])
def listar_zones():
    return repo.obtener_todos()


@router.get("/{zone_id}", dependencies=[Depends(require_permission("irrigation_zones", "ver"))])
def obtener_zone(zone_id: int):
    zone = repo.obtener_por_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zona de riego no encontrada")
    return zone


@router.get(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("irrigation_zones", "ver"))],
)
def listar_zones_por_greenhouse(greenhouse_id: int):
    return repo.obtener_por_greenhouse(greenhouse_id)


@router.post("/", dependencies=[Depends(require_permission("irrigation_zones", "crear"))])
def crear_zone(zone: IrrigationZoneCreate):
    nuevo_id = repo.crear(zone)
    return {"mensaje": "Zona de riego registrada exitosamente", "id": nuevo_id}


@router.put(
    "/{zone_id}", dependencies=[Depends(require_permission("irrigation_zones", "editar"))]
)
def actualizar_zone(zone_id: int, zone: IrrigationZoneUpdate):
    exito = repo.actualizar(zone_id, zone)
    if not exito:
        raise HTTPException(status_code=404, detail="Zona de riego no encontrada")
    return {"mensaje": "Zona de riego actualizada correctamente"}


@router.delete(
    "/{zone_id}", dependencies=[Depends(require_permission("irrigation_zones", "eliminar"))]
)
def eliminar_zone(zone_id: int):
    exito = repo.eliminar(zone_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Zona de riego no encontrada")
    return {"mensaje": "Zona de riego eliminada correctamente"}
