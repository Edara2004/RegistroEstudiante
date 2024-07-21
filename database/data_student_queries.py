import sqlite3
from admin_data_student.db_queries_student import DataQuery

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
	FOREIGN KEY (notes_students) REFERENCES data_user (id))
""")

connect_data.close()

# h = Student(3204565, "Marco Ayala", "2002-05-10", "Venezuela", "Masculino", "peppa_pig_magica@gmail.com", "Si", 5,"Sistemas")

print(DataQuery.get_student(31001145))
