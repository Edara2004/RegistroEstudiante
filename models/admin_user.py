class AdminUser:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def shw_ldts(self):
        return f"{self.username} {self.password}"

    def g_username(self):
        return self.username

    def g_password(self):
        return self.password

# r = AdminUser("Pepito", "1234")

# print(AdminUser.shw_ldts(r))
