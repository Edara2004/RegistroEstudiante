import bcrypt
import sqlite3


class AdminUser():
    def __init__(self, id_user: int, username: str, password: str):
        self.id_user = id_user
        self.username = username
        self.password = password

    def shw_ldts(self):
        return f"{self.username} {self.password}"

    def g_username(self):
        return self.username

    def g_password(self):
        return self.password

    def password_encrypt(self):
        text = self.password
        pwd = text.encode('utf-8')
        sal = bcrypt.gensalt()
        encrypt = bcrypt.hashpw(pwd, sal)

        return encrypt

    def get_password_encrypt(self):

        username = self.username

        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute("SELECT password from UserDB WHERE username =?", (username,))
            data_ = c.fetchone()
            pwd = data_[0]
            return pwd
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()


# r = AdminUser(129, 'Pepa', 'papa')
# print(AdminUser.get_password_encrypt(r))
