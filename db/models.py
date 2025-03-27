import sqlite3
import json
import bcrypt

from model.users.student import Student, RelatedPerson
from model.users.admin_user import AdminUser
from model.course.student_subjects import StudentSubjects


class CsControl(AdminUser):
    def __init__(self, db_path='..//student_data.db'):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    # Close Database

    def __del__(self):
        self.conn.close()

    # Insert new user

    def insert_new_user(self):
        try:
            self.c.execute(
                "INSERT INTO client VALUES (:username, :password, :secret_answer)",
                {
                    'username': self.username,  # Then encrypt
                    'password': self.password_encrypt(),
                    'secret_answer': self.secret_answer_encrypt()
                }
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            self.conn.close()

    # Update user Data -> Change password
    def update_user(self, username):
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            self.c.execute(f"UPDATE UserDB SET '{column_data}' = '{data_updating}' WHERE username= ?", (username,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.conn.close()

    # Delete user
    def delete_user(self, username):
        user_delete_data = input("¿Decide donde deseas eliminar?")
        try:
            self.c.execute(f"DELETE FROM UserDB WHERE {user_delete_data} = ?", (username,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.conn.close()

    def pass_user(self):

        get_password = self.get_password_encrypt()
        password = self.password
        vrf = bytes(password, 'utf-8')
        if bcrypt.checkpw(vrf, get_password):
            return True
        else:
            return False


class StudentManager(Student):
    def __init__(self, db_path='..//student_data.db'):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # Get Function

    @staticmethod
    def get_student(student_id):
        conn = sqlite3.connect("..//student_data.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM student WHERE student_id=?", (student_id,))
            data_ = c.fetchone()
            return data_
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    # Update function

    def update_student(student_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE data_user SET '{column_data}' = '{data_updating}' WHERE id= ?", (student_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Delete function
    def delete_student(student_id):
        conn = sqlite3.connect('..//student_data.db')
        c = conn.cursor()
        try:
            c.execute("DELETE FROM data_user WHERE career = ?", (student_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    # Insert function
    def insert_student(self):
        try:
            self.c.execute(
                "INSERT INTO students VALUES (:student_id, :student_fullname, :birthday, :address, :blood_type,"
                " :phone_number, :date_of_entry, :gender, :email, :nationality)",
                {
                    'student_id': self.student_id,
                    'student_fullname': self.student_fullname,
                    'birthday': self.student_birthday,
                    'address': self.student_address,
                    'blood_type': self.student_blood_type,
                    'phone_number': self.student_phone_number,
                    'date_of_entry': self.student_date_of_entry,
                    'gender': self.student_gender,
                    'email': self.student_email,
                    'nationality': self.student_nationality})
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            self.conn.close()


class StudentSubjectsManager(StudentSubjects):
    def __init__(self, db_path='..//student_data.db'):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    # Close Database

    def __del__(self):
        self.conn.close()

    # Create student
    def create_student(student_subjects_id, student_grade, notes):
        subjects_obj = StudentSubjectsManager(student_subjects_id, student_grade, notes)
        subjects_obj.insert_notes()

    # add and get notes
    def add_notes(self, subject, grade_value):
        self.notes[subject] = grade_value

    def get_notes(self):
        return self.notes

    # Insert notes
    def insert_notes(self):
        try:
            self.c.execute(
                "INSERT INTO subjects VALUES (:student_subjects_id, :student_grades, :student_notes)",
                {
                    'student_subjects_id': self.student_subjects_id,
                    'student_grades': self.student_grades,
                    # To insert a json with the notes
                    'student_notes': json.dumps(self.notes)
                })
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            self.conn.close()

    def get_students_subjects(self, student_subjects_id):
        try:
            self.c.execute(
                "SELECT student_subjects_id, student_grades, student_notes FROM subjects WHERE student_subjects_id = ?",
                (student_subjects_id,))
            row = self.c.fetchone()
            if row:
                student_subjects_id, student_grades, notes_json = row
                notes = json.loads(notes_json)
                return StudentSubjectsManager(student_subjects_id, student_grades, notes)
            else:
                return None
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            self.conn.close()

    # Update grades
    def update_student_notes(self, student_subjects_id, new_notes):
        update_subjects_obj = StudentSubjectsManager.get_subjects(student_subjects_id)
        if update_subjects_obj:
            update_subjects_obj.notes = new_notes
            self.c.execute(
                "UPDATE student_grades SET notes = ? WHERE student_subjects_id = ?",
                (json.dumps(update_subjects_obj.notes), student_subjects_id)
            )
            self.conn.commit()
            self.conn.close()

    # Get subjects
    def get_subjects(self):
        return list(self.notes.items())

    # Delete grades
    def delete_student(self, student_subjects_id):
        self.c.execute("DELETE FROM subjects WHERE student_subjects_id = ?", (student_subjects_id,))
        self.conn.commit()
        self.conn.close()

    # Get subjects by student
    def get_subjects_by_id(student_subjects_id):
        subjects = StudentSubjectsManager.get_students_subjects(student_subjects_id)
        if subjects:
            return subjects.get_subjects()
        else:
            return None


class RelatedPersonStudentManager(RelatedPerson):
    def __init__(self, db_path='..//student_data.db'):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()

    # CLose Database
    def __del__(self):
        self.conn.close()

    def insert_student(self):
        try:
            self.c.execute(
                "INSERT INTO legal_representative VALUES (:student_id, :related_person_id, :relationship_type, :fullname, :person_photo,"
                ":birthday, :blood_type, :phone_number, :job, :address, :marital_status, nationality)",
                {
                    'student_id': self.student_id,
                    'related_person_id': self.related_person_id,
                    'relationship_type': self.relationship_type,
                    'fullname': self.related_person_fullname,
                    'person_photo': self.related_person_photo,
                    'birthday': self.related_person_birthday,
                    'blood_type': self.related_person_blood_type,
                    'phone_number': self.related_person_phone_number,
                    'job': self.related_person_job,
                    'address': self.related_person_address,
                    'marital_status': self.related_person_marital_status,
                    'nationality': self.related_person_nationality
                })
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            self.conn.close()
