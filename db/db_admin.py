from models.admin_user import AdminUser
import sqlite3


class CsControl(AdminUser):
    def __init__(self, id_user: int, username: str, password: str):
        AdminUser.__init__(self, id_user, username, password)

    def insert_new_user(self):
        conn = sqlite3.connect('..//data_student.db')
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

    def update_user(username) -> None:
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        try:
            column_data = input("Write the column you use: ")  # input
            data_updating = input("Write the data you wanna change: ")  # input
            c.execute(f"UPDATE UserDB SET '{column_data}' = '{data_updating}' WHERE username= ?", (username,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    def delete_user(username) -> None:
        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        user_delete_data = input("¿Decide donde deseas eliminar?")
        try:
            c.execute(f"DELETE FROM UserDB WHERE {user_delete_data} = ?", (username,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    def pass_user(self):

        username = self.username
        password = self.password_encrypt()

        conn = sqlite3.connect('..//data_student.db')
        c = conn.cursor()
        statement = f"SELECT username from UserDB WHERE username = '{username}', AND password = '{password}'"
