import sqlite3
from database.user_data.db_queries_grade import GradeQueries
from models.grades_student import GradeStudent

# Connect to database
connect_data = sqlite3.connect('data_student.db')

cursor = connect_data.cursor()

# Create table if no exists

cursor.execute("""  CREATE TABLE IF NOT EXISTS grades_student (
	id_grade_student INTEGER NOT NULL,
	mathematics REAL,
	physics REAL,
	english REAL,
	chemistry REAL,
	time_grade TEXT,
	FOREIGN KEY (id_grade_student) REFERENCES data_user (id))
""")

# Close data

connect_data.close()

# Queries grade

# h = GradeStudent(25, 16, 15, 10, 11)

print(GradeQueries.get_notes(325))
