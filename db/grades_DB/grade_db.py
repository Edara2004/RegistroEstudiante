import sqlite3

from models.function_time.time_function import time_register
from models.grades_student import GradeStudent


class GradeQueries(GradeStudent):
    def __init__(self, id_grade_reference: int, id_grade_student: int, mathematics: int, physics: int, english: int,
                 chemistry: int, semester: int):
        sqlite3.__init__()
        super().__init__(id_grade_student, mathematics, physics, english, chemistry, semester)
        self.id_grade_reference = id_grade_reference

    # Get grades
    def get_notes(id_grade_reference) -> list:
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM grades_student WHERE id_grade_student=?", (id_grade_reference,))
            data_ = c.fetchone()
            return data_
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Insert grades
    def insert_notes(self):
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO grades_student VALUES (:id_grade_student, :mathematics, :physics, :english, :chemistry , :semester,:time)",
                {
                    'id_grade_student': self.id_grade_student,
                    'mathematics': self.mathematics,
                    'physics': self.physics,
                    'english': self.english,
                    'chemistry': self.chemistry,
                    'semester': self.semester,
                    'time': time_register()})
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Update grades
    def update_grade(id_grade_reference) -> None:
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE grades_student SET '{column_data}' = '{data_updating}' WHERE id_grade_student= ?",
                      (id_grade_reference,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Delete grades
    def delete_student(career_) -> None:
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        grade_delete_data = input("¿Decide donde deseas eliminar?")
        try:
            c.execute(f"DELETE FROM grades_student WHERE {grade_delete_data} = ?", (career_,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
