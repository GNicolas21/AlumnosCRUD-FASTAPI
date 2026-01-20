from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from src.data.db import SessionDep
from src.models.alumno import Alumno, AlumnoCreate, AlumnoResponse, Alumno
from src.data.alumnos_repository import AlumnosRepository
from src.models.alumno import map_create_to_alumno, map_alumno_to_response


router = APIRouter(prefix="/api/alumnos", tags=["alumnos"])

# Endpoint para listar todos los alumnos
@router.get("/", response_model = list[AlumnoResponse])
def listar_alumnos(session: SessionDep):
    # Obtener todos los alumnos de la "base de datos"
    repo = AlumnosRepository(session)
    alumnos = repo.get_all_alumnos()
    return [map_alumno_to_response(alumno) for alumno in alumnos]


@router.post("/", response_model=AlumnoResponse)
async def create_alumno(alumno_create: AlumnoCreate, session: SessionDep):
    # Verificar si el alumno ya existe
    repo = AlumnosRepository(session)
    alumno = map_create_to_alumno(alumno_create)
    alumno_creado = repo.create_alumno(alumno)
    return map_alumno_to_response(alumno_creado)

@router.get("/{alumno_id}", response_model=Alumno)
async def get_alumno_por_id(alumno_id: int, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return map_alumno_to_response(alumno_encontrado)

@router.delete("/{alumno_id}", status_code=204)
async def borrar_alumno(alumno_id: int, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    repo.delete_alumno(alumno_id)
    return {"mensaje": "Alumno eliminado correctamente"}

@router.patch("/{alumno_id}", response_model=Alumno, status_code=200)
async def actualizar_alumno(alumno_id: int, alumno:Alumno, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    # exclude_unset para actualizar solo los campos proporcionados
    alumno_data = alumno.model_dump(exclude_unset=True)
    # sqlmodel_update para actualizar el objeto existente
    alumno_encontrado.sqlmodel_update(alumno_data)
    repo.update_alumno(alumno_id, alumno_data)
    return map_alumno_to_response(alumno_encontrado)
