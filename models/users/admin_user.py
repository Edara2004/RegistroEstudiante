import bcrypt
import sqlite3


class AdminUser:
    def __init__(self, username: str, password: str, secret_answer: str):
        self.username = username
        self.password = password
        self.secret_answer = secret_answer

    def shw_ldts(self):
        return f"{self.username} {self.password}"

    def g_username(self):
        return self.username

    def g_password(self):
        return self.password

    # Password encrypts
    def password_encrypt(self):
        text_pwd = self.password
        pwd = text_pwd.encode('utf-8')
        sal = bcrypt.gensalt()
        encrypt_pw = bcrypt.hashpw(pwd, sal)

        return encrypt_pw

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

    # Secret answer encrypt
    def secret_answer_encrypt(self):
        text_sa = self.secret_answer
        pwd = text_sa.encode('utf-8')
        sal = bcrypt.gensalt()
        encrypt_sa = bcrypt.hashpw(pwd, sal)

        return encrypt_sa

    def get_secret_answer(self):

        username = self.username

        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            c.execute("SELECT secret_answer from client WHERE username =?", (username,))
            data_ = c.fetchone()
            # sa = Secret answer
            sa = data_[0]
            return sa
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()



#d = AdminUser(129, 'Pepa', 'papda')
#print(AdminUser.password_encrypt(d))
