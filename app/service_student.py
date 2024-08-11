import sqlalchemy
from sqlalchemy.orm import Session
from db.database import StudentData, Grade, Users
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from models.student import Student


class StudentService:

    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///./studentdb.db', echo=True, future=True)

    def register_student(self, id_student, name, birthday, nationality, gender, email, register, semester, career):
        student = Student()
        student.id_student = id_student
        student.name = name
        student.birthday = birthday
        student.nationality = nationality
        student.gender = gender
        student.email = email
        student.register = register
        student.semester = semester
        student.career = career
        with Session(self.engine) as session:
            session.add(student)
            session.commit()

    def modify_student(self, id_student_g, name, birthday, nationality, gender, email, register, semester, career):
        try:
            with Session(self.engine) as session:
                student = session.query(Student).filter_by(id=id_student_g).one()
                #
                student.name = name
                student.birthday = birthday
                student.nationality = nationality
                student.gender = gender
                student.email = email
                student.register = register
                student.semester = semester
                student.career = career

                session.commit()
                print(f'Los datos del id {id_student_g}, han sido actualizados exitosamente.')

        except NoResultFound as e:
            print(f'No se encontró ningún estudiante con esa ID, {id_student_g}. No se realizó ningún cambio')
        except Exception as e:
            print(f'Error al Actualizar el producto: {e}')
            return False

    def get_student(self) -> List[Student]:
        students: Student = None
        with Session(self.engine) as session:
            students = session.query(Student).all()
        return students

    def delete_student(self, id_student_g):
        with Session(self.engine) as session:
            student = session.query(Student).filter_by(id=id_student_g).first()
            if student:
                try:
                    session.delete(student)
                    session.commit()
                    print(f'El estudiante con la ID {id_student_g} fue eliminado correctamente.')

                except IntegrityError as e:
                    session.rollback()
                    print(f'No se pudo eliminar el estudiante con la ID {id_student_g}, Error {e}.')

                else:
                    print(f'No existe estudiante con la ID {id_student_g}')
