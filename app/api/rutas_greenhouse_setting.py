from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_permission
from app.models.greenhouse_setting import GreenhouseSetting, GreenhouseSettingCreate, GreenhouseSettingUpdate
from app.repositories.greenhouse_setting_repo import GreenhouseSettingRepository

router = APIRouter(prefix="/greenhouse-settings", tags=["Configuraciones"])
repo = GreenhouseSettingRepository()

@router.get("/", dependencies=[Depends(require_permission("greenhouse_settings", "ver"))])
async def listar_settings():
    return await repo.obtener_todos()

@router.get("/{setting_id}", dependencies=[Depends(require_permission("greenhouse_settings", "ver"))])
async def obtener_setting(setting_id: int):
    setting = await repo.obtener_por_id(setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return setting

@router.get("/greenhouse/{greenhouse_id}", dependencies=[Depends(require_permission("greenhouse_settings", "ver"))])
async def obtener_setting_por_greenhouse(greenhouse_id: int):
    setting = await repo.obtener_por_greenhouse(greenhouse_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada para este invernadero")
    return setting

@router.post("/", dependencies=[Depends(require_permission("greenhouse_settings", "crear"))])
async def crear_setting(setting: GreenhouseSettingCreate):
    nuevo_id = await repo.crear(setting)
    return {"mensaje": "Configuración creada exitosamente", "id": nuevo_id}

@router.put("/greenhouse/{greenhouse_id}", dependencies=[Depends(require_permission("greenhouse_settings", "editar"))])
async def actualizar_setting(greenhouse_id: int, setting: GreenhouseSettingUpdate):
    exito = await repo.actualizar(greenhouse_id, setting)
    if not exito:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return {"mensaje": "Configuración actualizada correctamente"}

@router.delete("/greenhouse/{greenhouse_id}", dependencies=[Depends(require_permission("greenhouse_settings", "eliminar"))])
async def eliminar_setting(greenhouse_id: int):
    if not await repo.eliminar_por_greenhouse(greenhouse_id):
        raise HTTPException(status_code=404, detail="Configuracion no encontrada")
    return {"mensaje": "Configuracion eliminada correctamente"}
