from fastapi import APIRouter, HTTPException
from app.models.crop_batch import CropBatch, CropBatchCreate, CropBatchUpdate
from app.repositories.crop_batch_repo import CropBatchRepository

router = APIRouter(prefix="/crop-batches", tags=["Lotes de Cultivos"])
repo = CropBatchRepository()

@router.get("/")
async def listar_batches():
    return await repo.obtener_todos()

@router.get("/{batch_id}")
async def obtener_batch(batch_id: int):
    batch = await repo.obtener_por_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return batch

@router.get("/greenhouse/{greenhouse_id}")
async def listar_batches_por_greenhouse(greenhouse_id: int):
    return await repo.obtener_por_greenhouse(greenhouse_id)

@router.post("/")
async def crear_batch(batch: CropBatchCreate):
    nuevo_id = await repo.crear(batch)
    return {"mensaje": "Lote registrado exitosamente", "id": nuevo_id}

@router.put("/{batch_id}")
async def actualizar_batch(batch_id: int, batch: CropBatchUpdate):
    exito = await repo.actualizar(batch_id, batch)
    if not exito:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote actualizado correctamente"}

@router.delete("/{batch_id}")
async def eliminar_batch(batch_id: int):
    exito = await repo.eliminar(batch_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote eliminado correctamente"}
