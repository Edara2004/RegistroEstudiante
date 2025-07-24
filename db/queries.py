from db.models import CsControl
from model.users.admin_user import AdminUser
from model.course.student_subjects import StudentSubjects
from db.models import StudentSubjectsManager, CsControl
import sqlite3

def add_student(nombre, apellido, edad, db_path="student_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            edad INTEGER
        )
    """)
    cursor.execute(
        "INSERT INTO estudiantes (nombre, apellido, edad) VALUES (?, ?, ?)",
        (nombre, apellido, edad)
    )
    conn.commit()
    conn.close()

# Elimina o comenta el código de prueba para evitar ejecuciones no deseadas
# h1 = AdminUser('Hola', "Guapa", "Te ví")
# print(CsControl.insert_new_user(h1))
