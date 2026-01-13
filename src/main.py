from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select


from src.data.db import init_db, get_sesion
from src.models.alumno import Alumno, AlumnoCreate, AlumnoResponse, AlumnoUpdate, map_create_to_alumno, map_update_to_alumno, map_alumno_to_response
from src.data.alumnos_repository import AlumnosRepository

import uvicorn

# Simulación de una base de datos en memoria
@asynccontextmanager
async def lifespan(application: FastAPI):
    # Inicializar la base de datos al iniciar la aplicación
    init_db()
    yield


# Lista en memoria para almacenar los alumnos
SessionDep = Annotated[Session, Depends(get_sesion)]    

# Crear la instancia de la aplicación FastAPI
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


# Endpoint para listar todos los alumnos
@app.get("/alumnos", response_model = list[AlumnoResponse])
def listar_alumnos(session: SessionDep):
    # Obtener todos los alumnos de la "base de datos"
    repo = AlumnosRepository(session)
    alumnos = repo.get_all_alumnos()
    return [map_alumno_to_response(alumno) for alumno in alumnos]


@app.post("/alumnos", response_model=AlumnoResponse)
async def create_alumno(alumno_create: AlumnoCreate, session: SessionDep):
    # Verificar si el alumno ya existe
    repo = AlumnosRepository(session)
    alumno = map_create_to_alumno(alumno_create)
    alumno_creado = repo.create_alumno(alumno)
    return map_alumno_to_response(alumno_creado)

@app.get("/alumnos/{alumno_id}", response_model=Alumno)
def get_alumno_por_id(alumno_id: int, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return map_alumno_to_response(alumno_encontrado)

@app.delete("/alumnos/{alumno_id}", status_code=204)
def borrar_alumno(alumno_id: int, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    repo.delete_alumno(alumno_id)
    return {"mensaje": "Alumno eliminado correctamente"}

@app.patch("/alumnos/{alumno_id}", response_model=Alumno, status_code=200)
def actualizar_alumno(alumno_id: int, alumno:Alumno, session: SessionDep):
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


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)