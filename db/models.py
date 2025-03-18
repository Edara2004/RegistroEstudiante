import sqlite3
import json
import bcrypt

from model.users.student import Student
from model.users.admin_user import AdminUser
from model.course.student_subjects import StudentSubjects


class CsControl(AdminUser):
    def __init__(self, id_user, username, password):
        AdminUser.__init__(self, id_user, username, password)

    def insert_new_user(self):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO client VALUES (:username, :password, :secret_answer)",
                {
                    'username': self.username,
                    'password': self.password_encrypt(),
                    'secret_answer': self.secret_answer_encrypt()
                }
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    def update_user(username):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE UserDB SET '{column_data}' = '{data_updating}' WHERE username= ?", (username,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    def delete_user(username):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        user_delete_data = input("¿Decide donde deseas eliminar?")
        try:
            c.execute(f"DELETE FROM UserDB WHERE {user_delete_data} = ?", (username,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    def pass_user(self):

        get_password = self.get_password_encrypt()
        password = self.password
        vrf = bytes(password, 'utf-8')
        if bcrypt.checkpw(vrf, get_password):
            return True
        else:
            return False


class StudentData(Student):
    def __init__(self, student_id: int, student_fullname: str, student_birthday: str, student_address: str,
                 student_blood_type: str, student_phone_number: str, student_date_of_entry: str,
                 student_gender: str, student_email: str, student_nationality: str):
        Student.__init__(self, student_id, student_fullname, student_birthday, student_address, student_blood_type,
                         student_phone_number, student_date_of_entry, student_gender,
                         student_email, student_nationality)

    # Connect Database

    @staticmethod
    def connect_data_base():
        conn = sqlite3.connect("..//student_data.db")
        cursor = conn.cursor()
        return conn, cursor

    # Get Function

    def get_student(student_id):
        conn = sqlite3.connect("..//student_data.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM student WHERE student_id=?", (student_id,))
            data_ = c.fetchone()
            return data_
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Update function

    def update_student(student_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE data_user SET '{column_data}' = '{data_updating}' WHERE id= ?", (student_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Delete function
    def delete_student(student_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute("DELETE FROM data_user WHERE career = ?", (student_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Insert function
    def insert_student(self):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO students VALUES (:student_id, :student_fullname, :birthday, :address, :blood_type,"
                " :phone_number, :date_of_entry, :gender, :email, :nationality)",
                {
                    'student_id': self.student_id,
                    'student_fullname': self.student_fullname,
                    'birthday': self.student_birthday,
                    'address': self.student_address,
                    'blood_type': self.student_blood_type,
                    'phone_number': self.student_phone_number,
                    'date_of_entry': self.student_date_of_entry,
                    'gender': self.student_gender,
                    'email': self.student_email,
                    'nationality': self.student_nationality})
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()


class StudentSubjectsManager(StudentSubjects):
    def __init__(self, student_subjects_id: int, student_grades: str, notes=None):
        super().__init__(student_subjects_id, student_grades, notes)
        self.student_subjects_id = student_subjects_id
        self.student_grade = student_grades
        self.notes = notes or {}

    # Create student
    def create_student(student_subjects_id, student_grade, notes):
        subjects_obj = StudentSubjectsManager(student_subjects_id, student_grade, notes)
        subjects_obj.insert_notes()

    # add and get notes
    def add_notes(self, subject, grade_value):
        self.notes[subject] = grade_value

    def get_notes(self):
        return self.notes

    # Insert notes
    def insert_notes(self):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO subjects VALUES (:student_subjects_id, :student_grades, :student_notes)",
                {
                    'student_subjects_id': self.student_subjects_id,
                    'student_grades': self.student_grade,
                    # To insert a json with the notes
                    'student_notes': json.dumps(self.notes)
                })
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_students_subjects(student_subjects_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute(
                "SELECT student_subjects_id, student_grades, student_notes FROM subjects WHERE student_subjects_id = ?",
                (student_subjects_id,))
            row = c.fetchone()
            if row:
                student_subjects_id, student_grades, notes_json = row
                notes = json.loads(notes_json)
                return StudentSubjectsManager(student_subjects_id, student_grades, notes)
            else:
                return None
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Update grades
    def update_student_notes(student_subjects_id, new_notes):
        grade_obj = StudentSubjects.get_grade(student_subjects_id)
        if grade_obj:
            grade_obj.notes = new_notes
            conn = sqlite3.connect('..//student_data.db')
            c = conn.cursor()
            c.execute(
                "UPDATE student_grades SET notes = ? WHERE student_subjects_id = ?",
                (json.dumps(grade_obj.notes), student_subjects_id)
            )
            conn.commit()
            conn.close()

    # Get subjects
    def get_subjects(self):
        return list(self.notes.keys())

    # Delete grades
    @staticmethod
    def delete_student(student_subjects_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        c.execute("DELETE FROM subjects WHERE student_subjects_id = ?", (student_subjects_id,))
        conn.commit()
        conn.close()

    # Get subjects by student
    @staticmethod
    def get_subjects_by_id(student_subjects_id):
        subjects = StudentSubjects.get_subjects(student_subjects_id)
        if subjects:
            return subjects.get_subjects(student_subjects_id)
        else:
            return None

    # Close Database
    @staticmethod
    def close_database(conn):
        conn.close()


# It is to add a new column of x number
class AddSubjects:
    def __init__(self, table: str, column: str):
        self.table = table
        self.column = column

    def add_column(table: str, column: str):
        connect_db = sqlite3.connect('prueba3.db')
        cursor_db = connect_db.cursor()

        sql_statements_db = f"ALTER TABLE {table} ADD {column};"

        cursor_db.executescript(sql_statements_db)

        connect_db.close()

    def delete_column(table: str, column: str):
        connect_db = sqlite3.connect('prueba3.db')
        cursor_db = connect_db.cursor()

        sql_statements_db = f"ALTER TABLE {table} DROP COLUMN {column};"

        cursor_db.executescript(sql_statements_db)

        connect_db.close()

    def rename_column(table: str, column: str):
        connect_db = sqlite3.connect('prueba3.db')
        cursor_db = connect_db.cursor()

        sql_statements_db = f"ALTER TABLE {table} DROP COLUMN {column};"

        cursor_db.executescript(sql_statements_db)

        connect_db.close()



