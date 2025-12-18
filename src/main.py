from fastapi import FastAPI
from src.data.db import alumnos
from src.models.alumno import Alumno

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Students API"}

def find_by_id(alumno_id: int):
    for alumno in alumnos:
        if alumno.id == alumno_id:
            return alumno
    return None

def siguiente_id():
    if alumnos:
        return max(a.id for a in alumnos) + 1
    return 1

@app.get("/alumnos")
async def read_alumnos():
    return alumnos 

@app.post("/alumnos")
async def create_alumno(alumno: Alumno):
    alumno.id = siguiente_id()
    alumnos.append(alumno)
    return alumno

@app.patch("/alumnos/{alumno_id}")
async def update_alumno(alumno_id: int, updated_alumno:Alumno):
    existing_alumno = find_by_id(alumno_id)
    
    if existing_alumno is None:
        return{"error": "Alumno not found"}
    if updated_alumno.nombre:
        existing_alumno.nombre = updated_alumno.nombre
    if updated_alumno.apellido:
        existing_alumno.apellido = updated_alumno.apellido
    if updated_alumno.grado:
        existing_alumno.grado = updated_alumno.grado
    if updated_alumno.fecha_nacimiento:
        existing_alumno.fecha_nacimiento = updated_alumno.fecha_nacimiento
    if updated_alumno.tiene_asignaturas_pendientes is not None:
        existing_alumno.tiene_asignaturas_pendientes = updated_alumno.tiene_asignaturas_pendientes
    return existing_alumno

@app.delete("/alumnos/{alumno_id}", status_code=204)
async def delete_alumno(alumno_id: int):
    existing_alumno = find_by_id(alumno_id)
    if existing_alumno is None:
        return{"error": "Alumno not found"}
    alumnos.remove(existing_alumno)
    return