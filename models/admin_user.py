import bcrypt


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


# r = AdminUser("Pepito", "1234")
# print(AdminUser.password_encrypt(r))
