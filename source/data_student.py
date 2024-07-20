import sqlite3
from ctr_data.Student import Student
from admin_data_student.dataquery import DataQuery

# Connect to source
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
	FOREIGN KEY (notes_students) REFERENCES data_user (id))
""")

# Insert Data into SQL

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

#h = Student(3204565, "Marco Ayala", "2002-05-10", "Venezuela", "Masculino", "peppa_pig_magica@gmail.com", "Si", 5,"Sistemas")

print(DataQuery.get_student(31001145))
