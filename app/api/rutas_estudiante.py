from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_permission
from app.models.estudiante import EstudianteCreate, EstudianteUpdate
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/estudiantes", tags=["Gestion de Estudiantes"])
repo = EstudianteRepository()


@router.get("/", dependencies=[Depends(require_permission("estudiantes", "ver"))])
def listar_estudiantes():
    return repo.obtener_todos()


@router.get(
    "/{estudiante_id}", dependencies=[Depends(require_permission("estudiantes", "ver"))]
)
def obtener_estudiante(estudiante_id: int):
    estudiante = repo.obtener_por_id(estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.post("/", dependencies=[Depends(require_permission("estudiantes", "crear"))])
def crear_estudiante(estudiante: EstudianteCreate):
    nuevo_id = repo.crear(estudiante)
    return {"mensaje": "Estudiante registrado exitosamente", "id": nuevo_id}


@router.put(
    "/{estudiante_id}", dependencies=[Depends(require_permission("estudiantes", "editar"))]
)
def actualizar_estudiante(estudiante_id: int, estudiante: EstudianteUpdate):
    exito = repo.actualizar(estudiante_id, estudiante)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante actualizado correctamente"}


@router.delete(
    "/{estudiante_id}",
    dependencies=[Depends(require_permission("estudiantes", "eliminar"))],
)
def eliminar_estudiante(estudiante_id: int):
    exito = repo.eliminar(estudiante_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante eliminado correctamente"}
