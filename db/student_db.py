import sqlite3
from typing import Any

from models.student import Student
from models.function_time.time_function import time_register


class StudentQuery(Student):
    def __init__(self, id_reference: int, career_: str, db_dir: str):
        sqlite3.__init__()
        super().__init__(self, id_student, name, birthday, nationality, gender, email, register, semester, career)
        self.id_reference = id_reference
        self.career_ = career_
        self.db_dir = db_dir

    # Connect Database

    def connect_data_base(self) -> None:
        conn = sqlite3.connect("..//data_student.db")
        cursor = conn.cursor()
        return conn, cursor

    # Get Function

    def get_student(id_reference) -> Any | None:
        conn = sqlite3.connect("..//data_student.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM data_user WHERE id=?", (id_reference,))
            data_ = c.fetchone()
            return data_
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Update function

    def update_student(id_reference) -> None:
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE data_user SET '{column_data}' = '{data_updating}' WHERE id= ?", (id_reference,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Delete function
    def delete_student(career_) -> None:
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute("DELETE FROM data_user WHERE career = ?", (career_,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Insert function
    def insert_student(self) -> None:
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO data_user VALUES (:id, :name, :birthday, :nationality, :gender, :email, :register, :semester, :career, :time)",
                {
                    'id': self.id_student,
                    'name': self.name,
                    'birthday': self.birthday,
                    'nationality': self.nationality,
                    'gender': self.gender,
                    'email': self.email,
                    'register': self.register,
                    'semester': self.semester,
                    'career': self.career,
                    'time': time_register()})
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Close Database function
    def close_database(self, conn):
        conn.close()
