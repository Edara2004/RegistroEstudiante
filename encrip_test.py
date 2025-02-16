import bcrypt
import sqlite3
from db.db_admin import AdminUser


connect_data = sqlite3.connect('prueba2.db')
cursor = connect_data.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS UserDB (
id_user INTEGER,
username TEXT NOT NULL,
password TEXT NOT NULL,
PRIMARY KEY("id_user"),
FOREIGN KEY (id_user) REFERENCES data_user (id)) """)

connect_data.close()

d = AdminUser(129, 'Pepa', 'papda')


class CsControl(AdminUser):
    def __init__(self, username: str, password: str):
        AdminUser.__init__(self, username, password)

    def insert_new_user(self):
        conn = sqlite3.connect('prueba2.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO UsserDB VALUES (:id_user, :username, :password)",
                {
                    'id_user': self.id_user,
                    'username': self.username,
                    'password': self.password_encrypt()
                }
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

    def pass_user(self):

        get_password = self.get_password_encrypt()
        password = self.password
        vrf = bytes(password, 'utf-8')
        if bcrypt.checkpw(vrf, get_password):
            print('Si')
        else:
            print('No, lee que hiciste')


print(CsControl.pass_user(d))
