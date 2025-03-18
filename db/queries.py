from models import CsControl
from model.users.admin_user import AdminUser

h1 = AdminUser("pep2", "12345", "hola")

print(CsControl.insert_new_user(h1))