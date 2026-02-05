from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Form
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime


from data.db import init_db, get_sesion
from models.alumno import Alumno, AlumnoCreate, AlumnoResponse, AlumnoUpdate, map_create_to_alumno, map_update_to_alumno, map_alumno_to_response
from data.alumnos_repository import AlumnosRepository
from routers.api_alumnos_router import router as api_alumnos_router

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
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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



@app.get("/alumnos/new", response_class=HTMLResponse)
async def nuevo_alumno_form(request: Request):
    # Renderizar el formulario para crear un nuevo alumno
    return templates.TemplateResponse("alumnos/alumno_form.html", {
        "request": request,
        "alumno": Alumno() 
        })

@app.post("/alumnos/new", response_class=HTMLResponse)
async def crear_alumno(request: Request, session: SessionDep):
    form_data = await request.form()
    nombre = form_data.get("nombre")
    grado = form_data.get("grado")
    fecha_nacimiento_str = form_data.get("fecha_nacimiento")
    tiene_asignaturas_pendientes_str = form_data.get("tiene_asignaturas_pendientes")
    
    # Convertir fecha de string a date object
    fecha_nacimiento = None
    if fecha_nacimiento_str:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido")
    
    # Convertir checkbox a boolean
    tiene_asignaturas_pendientes = tiene_asignaturas_pendientes_str == "on" if tiene_asignaturas_pendientes_str else False
    
    alumno_create = AlumnoCreate(
        nombre=nombre,
        grado=grado,
        fecha_nacimiento=fecha_nacimiento,
        tiene_asignaturas_pendientes=tiene_asignaturas_pendientes
    )
    
    repo = AlumnosRepository(session)
    alumno = map_create_to_alumno(alumno_create)
    
    repo.create_alumno(alumno)
    
    return RedirectResponse(url="/alumnos", status_code=303)
    
@app.get("/alumnos/{alumno_id}", response_class=HTMLResponse)
async def alumno_por_id(alumno_id: int, request: Request, session: SessionDep):
    repo = AlumnosRepository(session)
    alumno_encontrado = repo.get_alumno(alumno_id)
    if alumno_encontrado is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    alumno_response = map_alumno_to_response(alumno_encontrado)
    return templates.TemplateResponse("alumnos/alumno_detalle.html", {"request": request, "alumno": alumno_response})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)