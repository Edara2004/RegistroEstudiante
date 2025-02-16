import sqlite3
import bcrypt

from models.student import Student
from models.admin_user import AdminUser
from models.function_time.time_function import time_register
from models.grades_student import GradeStudent

# Connect to db
connect_data = sqlite3.connect('../data_student.db')

cursor = connect_data.cursor()

# Create table if no exists

sql_statements = """
CREATE TABLE IF NOT EXISTS data_user (
id	INTEGER,
name	TEXT NOT NULL,
birthday	TEXT NOT NULL,
nationality TEXT NOT NULL,
gender	TEXT NOT NULL,
email	TEXT NOT NULL,
register	TEXT,
semester	INTEGER NOT NULL,
career	TEXT NOT NULL,
time TEXT,
PRIMARY KEY("id" AUTOINCREMENT));
	
CREATE TABLE IF NOT EXISTS grades_student (
id_grade_student INTEGER NOT NULL,
mathematics REAL,
physics REAL,
english REAL,
chemistry REAL,
semester REAL,
time_grade TEXT,
FOREIGN KEY (id_grade_student) REFERENCES data_user (id));

CREATE TABLE IF NOT EXISTS UserDB (
id_user INTEGER,
username TEXT NOT NULL,
password TEXT NOT NULL,
PRIMARY KEY("id_user" AUTOINCREMENT),
FOREIGN KEY (id_user) REFERENCES data_user (id)) 
"""

cursor.executescript(sql_statements)

connect_data.close()


class CsControl(AdminUser):
    def __init__(self, id_user, username, password):
        AdminUser.__init__(self, id_user, username, password)

    def insert_new_user(self):
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO UserDB VALUES (:id_user, :username, :password)",
                {
                    'id_user': self.id_user,
                    'username': self.username,
                    'password': self.password_encrypt()
                }
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    def update_user(username):
        conn = sqlite3.connect('..//data_student.db')
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
        conn = sqlite3.connect('..//data_student.db')
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


class GradeQueries(GradeStudent):
    def __init__(self, id_grade_reference: int, id_grade_student: int, mathematics: int, physics: int, english: int,
                 chemistry: int, semester: int):
        sqlite3.__init__()
        super().__init__(id_grade_student, mathematics, physics, english, chemistry, semester)
        self.id_grade_reference = id_grade_reference

    # Get grades
    def get_notes(id_grade_reference) -> list:
        conn = sqlite3.connect('..//data_student.db')
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
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO grades_student VALUES (:id_grade_student, :mathematics, :physics, :english, :chemistry , :semester, :time)",
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
    def update_grade(id_grade_reference):
        conn = sqlite3.connect('..//data_student.db')
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
    def delete_student(career_):
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        grade_delete_data = input("¿Decide donde deseas eliminar?")  # Input
        try:
            c.execute(f"DELETE FROM grades_student WHERE {grade_delete_data} = ?", (career_,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


class StudentQuery(Student):
    def __init__(self, id_reference: int, career_: str, id_student, name, birthday, nationality, gender, email,
                 register, semester, career):
        sqlite3.__init__()
        Student.__init__(self, id_student, name, birthday, nationality, gender, email, register, semester, career)
        self.id_reference = id_reference
        self.career_ = career_

    # Connect Database

    def connect_data_base(self):
        conn = sqlite3.connect("..//data_student.db")
        cursor = conn.cursor()
        return conn, cursor

    # Get Function

    def get_student(id_reference):
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

    def update_student(id_reference):
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
    def delete_student(career_):
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
    def insert_student(self):
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


d = AdminUser(310001122, 'Pepa', 'passpda')
print(CsControl.insert_new_user(d))
