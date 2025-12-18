from src.models.alumno import Alumno
# Session es utilizado para interacciones con la base de datos
# create_engine para crear la conexión a la base de datos
# SQLModel es la clase base para los modelos de datos
from sqlmodel import create_engine, SQLModel, Session


db_user: str = "user"
db_password: str = "1234"
db_server: str = "localhost"
db_port: int = 3306
db_name: str = "alumnosdb"

#DATABASE_URL para la conexión a la base de datos MySQL
DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_sesion():
    # Crear el motor de la base de datos
    with Session(engine) as session:
        # Proveer la sesión para interacciones con la base de datos
        yield session

def init_db():
    # Eliminar las tablas existentes en la base de datos (si las hay)
    SQLModel.metadata.drop_all(engine)
    # Crear las tablas en la base de datos basadas en los modelos definidos
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Alumno(id=1, nombre="Antonio", grado="1º", fecha_nacimiento="2002-01-01", tiene_asignaturas_pendientes=False))
        session.add(Alumno(id=2, nombre="María", grado="2º", fecha_nacimiento="2005-05-05", tiene_asignaturas_pendientes=True))
        session.add(Alumno(id=3, nombre="Luis", grado="3º", fecha_nacimiento="2004-03-03", tiene_asignaturas_pendientes=False))
        session.commit()
        # session.refresh_all
        
