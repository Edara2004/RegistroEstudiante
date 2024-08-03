import sqlite3
from db.grades_DB.grade_db import GradeQueries


def db_connect_grade():
    # Connect to db
    connect_data = sqlite3.connect('data_student.db')

    # cursor

    cursor = connect_data.cursor()

    # Create table if no exists

    cursor.execute("""  CREATE TABLE IF NOT EXISTS grades_student (
        id_grade_student INTEGER NOT NULL,
        mathematics REAL,
        physics REAL,
        english REAL,
        chemistry REAL,
        semester REAL,
        time_grade TEXT,
        FOREIGN KEY (id_grade_student) REFERENCES data_user (id))
    """)

    # Close data

    connect_data.close()


# Queries grade

# h = GradeStudent(32, 16, 15, 10, 11, 1)
def g(id):
    db_connect_grade()
    gd = GradeQueries.get_notes(id)
    return gd


print(g(325))
