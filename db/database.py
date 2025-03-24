import sqlite3

# Connect to db
connect_data = sqlite3.connect('..//student_data.db')
cursor = connect_data.cursor()

# Create table if no exists

sql_statements = """
CREATE TABLE IF NOT EXISTS client (
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
secret_answer TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS students (
student_id INTEGER UNIQUE,
student_fullname TEXT NOT NULL,
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
student_id INTEGER NOT NULL,
student_grades TEXT,
student_notes TEXT,
FOREIGN KEY (student_id) REFERENCES students (student_id));

CREATE TABLE IF NOT EXISTS student_relationship (
student_id INTEGER NOT NULL,
related_person_id INTEGER NOT NULL,
relationship_type NOT NULL,
fullname TEXT NOT NULL,
person_photo BLOG,
birthday TEXT NOT NULL,
blood_type TEXT,
phone_number TEXT,
job TEXT,
address TEXT,
marital_status TEXT NOT NULL,
nationality TEXT,
FOREIGN KEY (student_id) REFERENCES students (student_id));

CREATE TABLE IF NOT EXISTS reports (
student_id INTEGER NOT NULL,
absences TEXT,
reports_details TEXT,
FOREIGN KEY (student_id) REFERENCES students (student_id)
)
"""

cursor.executescript(sql_statements)
connect_data.close()
