from sqlalchemy import create_engine, Column, Integer, String, INT, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base

sqlalchemy_database_url = "sqlite:///./studentdb.db"

engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(engine)
sessionlocal = SessionLocal()

base = declarative_base()


class StudentData(base):
    __tablename__ = 'student_data'

    id = Column(Integer(), primary_key=True, unique=True)
    name = Column(String(), nullable=False)
    birthday = Column(String(), nullable=False)
    nationality = Column(String(), nullable=False)
    gender = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    register = Column(String(), nullable=False)
    semester = Column(INT(), nullable=False)
    career = Column(String(), nullable=False)
    time = Column(DateTime(), default=datetime.now())


class Grade(base):
    __tablename__ = 'grade_student'

    id_grade = Column(Integer(), primary_key=True)
    id = Column(Integer(), ForeignKey('student_data.id'))
    mathematics = Column(INT())
    physics = Column(INT())
    english = Column(INT())
    chemistry = Column(INT())
    semester = Column(INT())
    time = Column(DateTime(), default=datetime.now())


class Users(base):
    __tablename__ = 'UserDB'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False)
    password = Column(String(), nullable=False)


if __name__ == '__main__':
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)
