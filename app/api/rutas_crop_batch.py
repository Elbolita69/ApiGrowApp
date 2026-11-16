from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.crop_batch import CropBatchCreate, CropBatchUpdate
from app.repositories.crop_batch_repo import CropBatchRepository

router = APIRouter(prefix="/crop-batches", tags=["Lotes de Cultivos"])
repo = CropBatchRepository()


@router.get("/", dependencies=[Depends(require_permission("crop_batches", "ver"))])
def listar_batches():
    return repo.obtener_todos()


@router.get("/{batch_id}", dependencies=[Depends(require_permission("crop_batches", "ver"))])
def obtener_batch(batch_id: int):
    batch = repo.obtener_por_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return batch


@router.get(
    "/greenhouse/{greenhouse_id}",
    dependencies=[Depends(require_permission("crop_batches", "ver"))],
)
def listar_batches_por_greenhouse(greenhouse_id: int):
    return repo.obtener_por_greenhouse(greenhouse_id)


@router.post("/", dependencies=[Depends(require_permission("crop_batches", "crear"))])
def crear_batch(batch: CropBatchCreate):
    nuevo_id = repo.crear(batch)
    return {"mensaje": "Lote registrado exitosamente", "id": nuevo_id}


@router.put(
    "/{batch_id}", dependencies=[Depends(require_permission("crop_batches", "editar"))]
)
def actualizar_batch(batch_id: int, batch: CropBatchUpdate):
    exito = repo.actualizar(batch_id, batch)
    if not exito:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote actualizado correctamente"}


@router.delete(
    "/{batch_id}", dependencies=[Depends(require_permission("crop_batches", "eliminar"))]
)
def eliminar_batch(batch_id: int):
    exito = repo.eliminar(batch_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"mensaje": "Lote eliminado correctamente"}
