import sqlite3

# Connect to db
connect_data = sqlite3.connect('../student_data.db')
cursor = connect_data.cursor()

# Create table if no exists

sql_statements = """
CREATE TABLE IF NOT EXISTS client (
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
secret_answer TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS students (
student_id INTEGER UNIQUE,
fullname_student TEXT NOT NULL,
birthday TEXT NOT NULL,
address TEXT NOT NULL,
blood_type TEXT,
phone_number TEXT,
date_of_entry TEXT,
gender TEXT NOT NULL,
email TEXT,
nationality TEXT NOT NULL,
PRIMARY KEY ("student_id")
);

CREATE TABLE IF NOT EXISTS subjects (
student_subjects_id INTEGER NOT NULL,
student_grades TEXT,
student_notes TEXT,
FOREIGN KEY (student_subjects_id) REFERENCES Students (student_id));

CREATE TABLE IF NOT EXISTS legal_representative (
legal_represented_id INTEGER NOT NULL,
legal_representative_id INTEGER,
legal_fullname TEXT NOT NULL,
legal_representative_photo BLOG,
legal_birthday TEXT NOT NULL,
legal_blood_type TEXT,
legal_phone_number TEXT,
legal_job TEXT,
legal_address TEXT,
legal_marital_status TEXT NOT NULL,
legal_nationality TEXT,
FOREIGN KEY (legal_represented_id) REFERENCES Students (student_id));

CREATE TABLE IF NOT EXISTS student_father (
father_student_id INTEGER NOT NULL,
father_id INTEGER NOT NULL,
father_fullname TEXT NOT NULL,
father_birthday TEXT NOT NULL,
father_blood_type TEXT,
father_phone_number TEXT NOT NULL,
father_job TEXT,
father_address TEXT,
father_marital_status TEXT NOT NULL,
father_nationality TEXT,
FOREIGN KEY (father_student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS student_mother (
mother_student_id INTEGER NOT NULL,
mother_id INTEGER NOT NULL,
mother_fullname TEXT NOT NULL,
mother_birthday TEXT NOT NULL,
mother_blood_type TEXT,
mother_phone_number TEXT NOT NULL,
mother_job TEXT,
mother_address TEXT,
mother_marital_status TEXT NOT NULL,
mother_nationality TEXT,
FOREIGN KEY (mother_student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS reports (
reports_student_id INTEGER NOT NULL,
absences TEXT,
reports_details TEXT,
FOREIGN KEY (reports_student_id) REFERENCES Students (student_id)
)
"""

cursor.executescript(sql_statements)
connect_data.close()
