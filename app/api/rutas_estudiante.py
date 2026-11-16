from fastapi import APIRouter, HTTPException
from app.models.estudiante import Estudiante
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/estudiantes", tags=["Gestión de Estudiantes"])
repo = EstudianteRepository()

@router.get("/")
async def listar_estudiantes():
    return await repo.obtener_todos()

@router.get("/{estudiante_id}")
async def obtener_estudiante(estudiante_id: int):
    estudiante = await repo.obtener_por_id(estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.post("/")
async def crear_estudiante(estudiante: Estudiante):
    nuevo_id = await repo.crear(estudiante)
    return {"mensaje": "Estudiante registrado exitosamente", "id": nuevo_id}

@router.delete("/{estudiante_id}")
async def eliminar_estudiante(estudiante_id: int):
    exito = await repo.eliminar(estudiante_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante eliminado correctamente"}

@router.put("/{estudiante_id}")
async def actualizar_estudiante(estudiante_id: int, estudiante: Estudiante):
    exito = await repo.actualizar(estudiante_id, estudiante)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante actualizado correctamente"}
