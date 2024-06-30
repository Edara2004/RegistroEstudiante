import sqlite3
from main import Student
from time_function import time_register
from dataquery import DataQuery

# Connect to source
connect_data = sqlite3.connect('data_student.db')

cursor = connect_data.cursor()

#Create table if no exists
cursor.execute(""" CREATE TABLE IF NOT EXISTS data_user (
	id	INTEGER,
	name	TEXT NOT NULL,
	birthday	TEXT NOT NULL,
	nationality TEXT NOT NULL,
	gender	TEXT NOT NULL,
	email	TEXT NOT NULL,
	register	TEXT,
	semestre	INTEGER NOT NULL,
	career	TEXT NOT NULL,
	time TEXT,
	PRIMARY KEY("id" AUTOINCREMENT))
""")

#cursor.execute("INSERT INTO data_user VALUES (3, 'Pedro Perez', '2004-11-11', 'Venezolano', 'Hombre', 'pepitoDa@gmail.com', 'Si', '1', 'Sistemas')")

# Insert Data into SQL

# est_1 = Student(7, "Alberto Rodriguez", "2002-11-23", "Peru", "Masculino", "daniel@gmail.com", "Si", 2, "Industrial")
#
# cursor.execute("INSERT INTO data_user VALUES (:id, :name, :birthday, :nacionality, :gender, :email, :register, :semester, :career, :time)",{
#     'id' : est_1.id,
#     'name' : est_1.name,
#     'birthday': est_1.birthday,
#     'nacionality' : est_1.nacionality,
#     'gender' : est_1.gender,
#     'email' : est_1.email,
#     'register' : est_1.register,
#     'semester' : est_1.semester,
#     'career' : est_1.career,
#     'time' : time_register()})

# Upload data
# connect_data.commit()



# Show data from source
# cursor.execute("SELECT * FROM data_user")
# estudiantes = cursor.fetchmany(10)
# print(estudiantes)

connect_data.close()

print(DataQuery.insert_student())
