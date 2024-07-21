import sqlite3

from ctr_data.function_time.time_function import time_register
from ctr_data.grades_student import Notes


class NotesQuery(Notes):
    def __init__(self, id_notes_reference: int, id_student_notes: int, mathematics: int, physics: int, english: int):
        sqlite3.__init__()
        super().__init__(id_student_notes, mathematics, physics, english)
        self.id_notes_reference = id_notes_reference

    def get_notes(id_notes_reference):
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM note_students WHERE id=?", (id_notes_reference,))
            data_ = c.fetchone()
            return data_
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    def insert_notes(self):
        conn = sqlite3.connect('data_student.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO note_students VALUES (:id, mathematics:, physics:, english:, :time)",
                {
                    'id': self.id_student_notes,
                    'mathematics': self.mathematics,
                    'physics': self.physics,
                    'english': self.english,
                    'time': time_register()})
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()
