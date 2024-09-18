import bcrypt
import sqlite3
from db.db_admin import AdminUser

# text = 'hola negretes'
# pwd = text.encode('utf-8')
# sal = bcrypt.gensalt()
# encript = bcrypt.hashpw(pwd, sal)

# pwd = b'$2b$12$kLEp6KzdKtdRRenrD6B3OOCuWxUEwLjqstzqj4oagwmrKoo3rvrSW'
#
# txt = bytes('hola negrete', 'utf-8')
# if bcrypt.checkpw(txt, pwd):
#     print('Joda')
# else:
#     print('Falta pa')

connect_data = sqlite3.connect('prueba.db')

cursor = connect_data.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS UserDB (
id_user INTEGER,
username TEXT NOT NULL,
password TEXT NOT NULL,
PRIMARY KEY("id_user" AUTOINCREMENT),
FOREIGN KEY (id_user) REFERENCES data_user (id)) """)

connect_data.close()

d = AdminUser(124, 'Pepe', 'papa')

class CsControl(AdminUser):
    def __init__(self, username: str, password: str):
        AdminUser.__init__(self, username, password)

    def insert_new_user(self):
        conn = sqlite3.connect('prueba.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO UserDB VALUES (:id_user, :username, :password)",
                {
                    'id_user': self.id_user,
                    'username': self.username,
                    'password': self.password_encrypt()})
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

print(CsControl.insert_new_user(d))