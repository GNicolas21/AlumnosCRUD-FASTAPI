from sqlmodel import Field, SQLModel
from datetime import date
from pydantic import BaseModel

class Alumno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index = True, max_length=50)
    grado: str = Field(index = True, max_length=100)
    fecha_nacimiento: date | None = Field(nullable=True) 
    tiene_asignaturas_pendientes: bool | None = Field(default=None, nullable=True)


# dto classes
class AlumnoCreate(BaseModel):
    nombre: str
    grado: str
    fecha_nacimiento: date | None = None
    tiene_asignaturas_pendientes: bool | None = None

class AlumnoUpdate(BaseModel):
    nombre: str | None = None
    grado: str | None = None
    fecha_nacimiento: date | None = None
    tiene_asignaturas_pendientes: bool | None = None

class AlumnoResponse(BaseModel):
    id: int
    nombre: str
    grado: str
    fecha_nacimiento: date | None = None
    tiene_asignaturas_pendientes: bool | None = None

# mapping functions
def map_alumno_to_response(alumno: Alumno) -> AlumnoResponse:
    return AlumnoResponse(
        id = alumno.id,
        nombre= alumno.nombre,
        grado= alumno.grado,
        fecha_nacimiento= alumno.fecha_nacimiento,
        tiene_asignaturas_pendientes= alumno.tiene_asignaturas_pendientes
    )

def map_create_to_alumno(alumno_create: AlumnoCreate) -> Alumno:
    return Alumno(
        nombre = alumno_create.nombre,
        grado = alumno_create.grado,
        fecha_nacimiento= alumno_create.fecha_nacimiento,
        tiene_asignaturas_pendientes= alumno_create.tiene_asignaturas_pendientes
    )

def map_update_to_alumno(alumno: Alumno, alumno_update: AlumnoUpdate) -> Alumno:
    if alumno_update.nombre is not None:
        alumno.nombre = alumno_update.nombre
    if alumno_update.grado is not None:
        alumno.grado = alumno_update.grado
    if alumno_update.fecha_nacimiento is not None:
        alumno.fecha_nacimiento = alumno_update.fecha_nacimiento
    if alumno_update.tiene_asignaturas_pendientes is not None:
        alumno.tiene_asignaturas_pendientes = alumno_update.tiene_asignaturas_pendientes
    return alumno    