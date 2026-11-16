from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.greenhouse_setting import (
    GreenhouseSettingCreate,
    GreenhouseSettingUpdate,
)
from app.repositories.greenhouse_setting_repo import GreenhouseSettingRepository

router = APIRouter(prefix="/greenhouse-settings", tags=["Configuraciones"])
repo = GreenhouseSettingRepository()


@router.get("/", dependencies=[Depends(require_permission("greenhouse_settings", "ver"))])
def listar_settings():
    return repo.obtener_todos()


@router.get(
    "/{setting_id}", dependencies=[Depends(require_permission("greenhouse_settings", "ver"))]
)
def obtener_setting(setting_id: int):
    setting = repo.obtener_por_id(setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return setting


@router.get(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("greenhouse_settings", "ver"))],
)
def obtener_setting_por_greenhouse(greenhouse_id: int):
    setting = repo.obtener_por_greenhouse(greenhouse_id)
    if not setting:
        raise HTTPException(
            status_code=404, detail="Configuracion no encontrada para este invernadero"
        )
    return setting


@router.post("/", dependencies=[Depends(require_permission("greenhouse_settings", "crear"))])
def crear_setting(setting: GreenhouseSettingCreate):
    nuevo_id = repo.crear(setting)
    return {"mensaje": "Configuracion creada exitosamente", "id": nuevo_id}


@router.put(
    "/{setting_id}",
    dependencies=[Depends(require_permission("greenhouse_settings", "editar"))],
)
def actualizar_setting(setting_id: int, setting: GreenhouseSettingUpdate):
    exito = repo.actualizar(setting_id, setting)
    if not exito:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return {"mensaje": "Configuracion actualizada correctamente"}


@router.put(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("greenhouse_settings", "editar"))],
)
def actualizar_setting_por_greenhouse(
    greenhouse_id: int, setting: GreenhouseSettingUpdate
):
    exito = repo.actualizar_por_greenhouse(greenhouse_id, setting)
    if not exito:
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return {"mensaje": "Configuracion actualizada correctamente"}


@router.delete(
    "/{setting_id}",
    dependencies=[Depends(require_permission("greenhouse_settings", "eliminar"))],
)
def eliminar_setting(setting_id: int):
    if not repo.eliminar(setting_id):
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return {"mensaje": "Configuracion eliminada correctamente"}


@router.delete(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("greenhouse_settings", "eliminar"))],
)
def eliminar_setting_por_greenhouse(greenhouse_id: int):
    if not repo.eliminar_por_greenhouse(greenhouse_id):
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return {"mensaje": "Configuracion eliminada correctamente"}
