from pydantic import BaseModel

class Alumno(BaseModel):
    id: int
    nombre: str
    apellido: str
    grado: str
    
    