from src.models.alumno import Alumno

alumnos : list[Alumno] = [
    Alumno(id=1, nombre="Antonio", apellido="Altimira", grado="1º", fecha_nacimiento="2002-01-01", tiene_asignaturas_pendientes=False),
    Alumno(id=2, nombre="María", apellido="Gómez", grado="2º", fecha_nacimiento="2005-05-05", tiene_asignaturas_pendientes=True),
    Alumno(id=3, nombre="Luis", apellido="Rodríguez", grado="3º", fecha_nacimiento="2004-03-03", tiene_asignaturas_pendientes=False),
]
