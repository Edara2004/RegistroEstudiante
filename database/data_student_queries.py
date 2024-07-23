import sqlite3
from database.student_DB.db_queries_student import StudentQuery
from models.student import Student

# Connect to database
connect_data = sqlite3.connect('data_student.db')

cursor = connect_data.cursor()

# Create table if no exists

cursor.execute(""" CREATE TABLE IF NOT EXISTS data_user (
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY (id_grade_student) REFERENCES data_user (id))	
""")

connect_data.close()

# h = Student(325, "Marco Ayala", "2002-05-10", "Venezuela", "Masculino", "peppa_pig_magica@gmail.com", "Si", 5,
#            "Sistemas")

print(StudentQuery.get_student(325))
