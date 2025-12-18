from pydantic import BaseModel
from datetime import date

class Alumno(BaseModel):
    id: int | None = None
    nombre: str | None = None
    apellido: str | None = None
    grado: str | None = None
    fecha_nacimiento: date | None = None
    tiene_asignaturas_pendientes: bool | None = None
    