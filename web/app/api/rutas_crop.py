from fastapi import APIRouter, HTTPException
from app.models.crop import Crop, CropCreate, CropUpdate
from app.repositories.crop_repo import CropRepository

router = APIRouter(prefix="/crops", tags=["Cultivos"])
repo = CropRepository()

@router.get("/")
async def listar_crops():
    return await repo.obtener_todos()

@router.get("/{crop_id}")
async def obtener_crop(crop_id: int):
    crop = await repo.obtener_por_id(crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return crop

@router.post("/")
async def crear_crop(crop: CropCreate):
    nuevo_id = await repo.crear(crop)
    return {"mensaje": "Cultivo registrado exitosamente", "id": nuevo_id}

@router.put("/{crop_id}")
async def actualizar_crop(crop_id: int, crop: CropUpdate):
    exito = await repo.actualizar(crop_id, crop)
    if not exito:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return {"mensaje": "Cultivo actualizado correctamente"}

@router.delete("/{crop_id}")
async def eliminar_crop(crop_id: int):
    exito = await repo.eliminar(crop_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return {"mensaje": "Cultivo eliminado correctamente"}
