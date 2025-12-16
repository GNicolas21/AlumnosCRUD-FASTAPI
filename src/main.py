from fastapi import FastAPI
from src.data.db import alumnos
from src.models.alumno import Alumno

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Students API"}

