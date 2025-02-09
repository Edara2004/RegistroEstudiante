import sqlite3
from db.student_db import StudentQuery
from db.grade_db import GradeQueries
from db.db_admin import AdminUser, CsControl
from models.grades_student import GradeStudent
from models.student import Student

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

# h = Student(327, "Marco Ayala", "2002-06-10", "Venezuela", "Masculino", "peppa_pig_magica@gmail.com", "Si", 5,
#           "Sistemas")

# print(StudentQuery.insert_student(h))

# d = GradeStudent(345, 12, 23, 12, 12, 5)

# h = AdminUser(136, 'Pepe', 'gana')

# print(CsControl.pass_user(h))
