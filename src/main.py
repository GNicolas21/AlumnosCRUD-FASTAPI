from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


from src.data.db import init_db, get_sesion
from src.models.alumno import Alumno, AlumnoCreate, AlumnoResponse, AlumnoUpdate, map_create_to_alumno, map_update_to_alumno, map_alumno_to_response
from src.data.alumnos_repository import AlumnosRepository
from src.routers.api_alumnos_router import router as api_alumnos_router

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

# Configuración de archivos estáticos y plantillas
# http://127.0.0.1:8000/static/static.html
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

# Incluir el router para la API de alumnos
app.include_router(api_alumnos_router)

#Ruta para página principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/alumnos", response_class=HTMLResponse)
async def ver_alumnos(request: Request, session: SessionDep):
    repo = AlumnosRepository(session)
    alumnos = repo.get_all_alumnos()
    return templates.TemplateResponse("alumnos/alumnos.html", {"request": request, "alumnos":alumnos})


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)