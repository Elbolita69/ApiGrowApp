from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.crop import CropCreate, CropUpdate
from app.repositories.crop_repo import CropRepository

router = APIRouter(prefix="/crops", tags=["Cultivos"])
repo = CropRepository()


@router.get("/", dependencies=[Depends(require_permission("crops", "ver"))])
def listar_crops():
    return repo.obtener_todos()


@router.get("/{crop_id}", dependencies=[Depends(require_permission("crops", "ver"))])
def obtener_crop(crop_id: int):
    crop = repo.obtener_por_id(crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return crop


@router.post("/", dependencies=[Depends(require_permission("crops", "crear"))])
def crear_crop(crop: CropCreate):
    nuevo_id = repo.crear(crop)
    return {"mensaje": "Cultivo registrado exitosamente", "id": nuevo_id}


@router.put("/{crop_id}", dependencies=[Depends(require_permission("crops", "editar"))])
def actualizar_crop(crop_id: int, crop: CropUpdate):
    exito = repo.actualizar(crop_id, crop)
    if not exito:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return {"mensaje": "Cultivo actualizado correctamente"}


@router.delete(
    "/{crop_id}", dependencies=[Depends(require_permission("crops", "eliminar"))]
)
def eliminar_crop(crop_id: int):
    exito = repo.eliminar(crop_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return {"mensaje": "Cultivo eliminado correctamente"}
