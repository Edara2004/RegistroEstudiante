import bcrypt
import sqlite3


class AdminUser:
    def __init__(self, username: str, password: str, secret_answer: str):
        self.username = username
        self.password = password
        self.secret_answer = secret_answer

    def show_data(self):
        return f" {self.username_encrypt()}\n {self.password_encrypt()}\n {self.secret_answer_encrypt()}"

    def g_username(self):
        return self.username

    def g_password(self):
        return self.password

    def g_secret_answer(self):
        return self.secret_answer

    # Password encrypts
    def password_encrypt(self):
        text_pwd = self.password
        pwd = text_pwd.encode('utf-8')
        sal = bcrypt.gensalt()
        encrypt_pw = bcrypt.hashpw(pwd, sal)

        return encrypt_pw

    def get_password_encrypt(self):

        username = self.username

        conn = sqlite3.connect('../../student_data.db')
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

        conn = sqlite3.connect('../../student_data.db')
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

    # Username encrypt
    def username_encrypt(self):
        text_user = self.username
        pwd = text_user.encode('utf-8')
        sal = bcrypt.gensalt()
        encrypt_user = bcrypt.hashpw(pwd, sal)

        return encrypt_user

    def get_username(self):

        username = self.username

        conn = sqlite3.connect('../../student_data.db')
        c = conn.cursor()
        try:
            c.execute("SELECT secret_answer from client WHERE username =?", (username,))
            data_ = c.fetchone()
            # Username encrypt
            ue = data_[0]
            return ue
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()
