from fastapi import APIRouter, HTTPException
from app.models.greenhouse import Greenhouse, GreenhouseCreate, GreenhouseUpdate
from app.repositories.greenhouse_repo import GreenhouseRepository

router = APIRouter(prefix="/greenhouses", tags=["Invernaderos"])
repo = GreenhouseRepository()

@router.get("/")
async def listar_greenhouses():
    return await repo.obtener_todos()

@router.get("/{greenhouse_id}")
async def obtener_greenhouse(greenhouse_id: int):
    greenhouse = await repo.obtener_por_id(greenhouse_id)
    if not greenhouse:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return greenhouse

@router.post("/")
async def crear_greenhouse(greenhouse: GreenhouseCreate):
    nuevo_id = await repo.crear(greenhouse)
    return {"mensaje": "Invernadero creado exitosamente", "id": nuevo_id}

@router.put("/{greenhouse_id}")
async def actualizar_greenhouse(greenhouse_id: int, greenhouse: GreenhouseUpdate):
    exito = await repo.actualizar(greenhouse_id, greenhouse)
    if not exito:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero actualizado correctamente"}

@router.delete("/{greenhouse_id}")
async def eliminar_greenhouse(greenhouse_id: int):
    exito = await repo.eliminar(greenhouse_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Invernadero no encontrado")
    return {"mensaje": "Invernadero eliminado correctamente"}
