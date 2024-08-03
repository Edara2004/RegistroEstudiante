import sqlite3
from admin_DB.db_admin import CsControl


# Connect db
connect_db = sqlite3.connect('admin_data.db')

# Cursor db
cursor = connect_db.cursor()

cursor.execute("""  CREATE TABLE IF NOT EXISTS data_admin (
    id_user INTEGER,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY("id_user" AUTOINCREMENT))
""")

# Close db
connect_db.close()


print(CsControl.update_user("Benito"))
