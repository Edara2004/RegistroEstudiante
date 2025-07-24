import sqlite3
import os
from db.queries import add_student

def test_add_student(tmp_path):
    # Usar una base de datos temporal
    test_db = tmp_path / "test_student_data.db"
    db_path = str(test_db)
    
    # Agregar un estudiante
    add_student("Ana", "García", 22, db_path=db_path)
    
    # Verificar que el estudiante fue agregado
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido, edad FROM estudiantes")
    result = cursor.fetchall()
    conn.close()
    
    assert len(result) == 1
    assert result[0] == ("Ana", "García", 22) 