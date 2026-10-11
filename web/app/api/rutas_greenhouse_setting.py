from fastapi import APIRouter, HTTPException
from app.models.greenhouse_setting import GreenhouseSetting, GreenhouseSettingCreate, GreenhouseSettingUpdate
from app.repositories.greenhouse_setting_repo import GreenhouseSettingRepository

router = APIRouter(prefix="/greenhouse-settings", tags=["Configuraciones"])
repo = GreenhouseSettingRepository()

@router.get("/")
async def listar_settings():
    return await repo.obtener_todos()

@router.get("/{setting_id}")
async def obtener_setting(setting_id: int):
    setting = await repo.obtener_por_id(setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return setting

@router.get("/greenhouse/{greenhouse_id}")
async def obtener_setting_por_greenhouse(greenhouse_id: int):
    setting = await repo.obtener_por_greenhouse(greenhouse_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada para este invernadero")
    return setting

@router.post("/")
async def crear_setting(setting: GreenhouseSettingCreate):
    nuevo_id = await repo.crear(setting)
    return {"mensaje": "Configuración creada exitosamente", "id": nuevo_id}

@router.put("/greenhouse/{greenhouse_id}")
async def actualizar_setting(greenhouse_id: int, setting: GreenhouseSettingUpdate):
    exito = await repo.actualizar(greenhouse_id, setting)
    if not exito:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return {"mensaje": "Configuración actualizada correctamente"}
