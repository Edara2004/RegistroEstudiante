import sqlite3

# Connect db
connect_db = sqlite3.connect('admin_data.db')

# Cursor db
cursor = connect_db.cursor()

cursor.execute("""  CREATE TABLE IF NOT EXISTS data_admin (
    username TEXT NOT NULL,
    password TEXT NOT NULL)
""")

# Close db
connect_db.close()
