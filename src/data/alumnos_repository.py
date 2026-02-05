from sqlmodel import Session, select
from src.models.alumno import Alumno

class AlumnosRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_alumnos(self) -> list[Alumno]:
        alumnos = self.session.exec(select(Alumno)).all()
        return alumnos
    
    def get_alumno(self, alumno_id: int) -> Alumno:
        alumno = self.session.get(Alumno, alumno_id)
        return alumno
    
    def create_alumno(self, alumno: Alumno) -> Alumno:
        self.session.add(alumno)
        self.session.commit()
        self.session.refresh(alumno)
        return alumno
    
    def update_alumno(self, alumno_id: int, alumno_data: dict) -> Alumno:
        alumno = self.get_alumno(alumno_id)
        if alumno:
            for key, value in alumno_data.items():
                setattr(alumno, key, value)
            self.session.commit()
            self.session.refresh(alumno)
        return alumno
    
    def delete_alumno(self, alumno_id: int) -> None:
        alumno = self.get_alumno(alumno_id)
        self.session.delete(alumno)
        self.session.commit()