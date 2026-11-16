from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.greenhouse import GreenhouseCreate, GreenhouseUpdate
from app.repositories.greenhouse_repo import GreenhouseRepository

router = APIRouter(prefix="/greenhouses", tags=["Invernaderos"])
repo = GreenhouseRepository()


@router.get("/", dependencies=[Depends(require_permission("greenhouses", "ver"))])
def listar_greenhouses():
    return repo.obtener_todos()


@router.get(
    "/{greenhouse_id}", dependencies=[Depends(require_permission("greenhouses", "ver"))]
)
def obtener_greenhouse(greenhouse_id: int):
    greenhouse = repo.obtener_por_id(greenhouse_id)
    if not greenhouse:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return greenhouse


@router.post("/", dependencies=[Depends(require_permission("greenhouses", "crear"))])
def crear_greenhouse(greenhouse: GreenhouseCreate):
    nuevo_id = repo.crear(greenhouse)
    return {"mensaje": "Invernadero creado exitosamente", "id": nuevo_id}


@router.put(
    "/{greenhouse_id}", dependencies=[Depends(require_permission("greenhouses", "editar"))]
)
def actualizar_greenhouse(greenhouse_id: int, greenhouse: GreenhouseUpdate):
    exito = repo.actualizar(greenhouse_id, greenhouse)
    if not exito:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero actualizado correctamente"}


@router.delete(
    "/{greenhouse_id}",
    dependencies=[Depends(require_permission("greenhouses", "eliminar"))],
)
def eliminar_greenhouse(greenhouse_id: int):
    exito = repo.eliminar(greenhouse_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero eliminado correctamente"}
