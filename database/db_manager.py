import sqlite3
import bcrypt
import os

class DatabaseManager:
    def __init__(self, db_path='student_data.db'):
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Asegura que la base de datos y las tablas existan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client (
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                secret_answer TEXT NOT NULL
            )
        """)
        
        # Crear tabla de estudiantes si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER UNIQUE,
                student_fullname TEXT NOT NULL,
                birthday TEXT NOT NULL,
                address TEXT NOT NULL,
                blood_type TEXT,
                phone_number TEXT,
                date_of_entry TEXT,
                gender TEXT NOT NULL,
                email TEXT,
                nationality TEXT NOT NULL,
                PRIMARY KEY ("student_id")
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_user(self, username, password, admin_password):
        """Registra un nuevo usuario en la base de datos"""
        try:
            # Verificar contraseña admin
            from config.theme import ADMIN_PASSWORD
            if admin_password != ADMIN_PASSWORD:
                return False, "¡Ups! La contraseña de administrador no es correcta. Por favor, verifica e intenta nuevamente."
            
            # Encriptar contraseña
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            
            # Encriptar username
            username_bytes = username.encode('utf-8')
            hashed_username = bcrypt.hashpw(username_bytes, salt)
            
            # Encriptar secret answer (usando admin_password como secret_answer)
            secret_bytes = admin_password.encode('utf-8')
            hashed_secret = bcrypt.hashpw(secret_bytes, salt)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO client (username, password, secret_answer) VALUES (?, ?, ?)",
                (hashed_username, hashed_password, hashed_secret)
            )
            
            conn.commit()
            conn.close()
            return True, "¡Excelente! Tu cuenta ha sido creada exitosamente. Ya puedes iniciar sesión."
            
        except sqlite3.IntegrityError:
            return False, "Este nombre de usuario ya está en uso. Por favor, elige otro nombre de usuario."
        except Exception as e:
            return False, f"Lo sentimos, hubo un problema al crear tu cuenta. Por favor, intenta nuevamente."
    
    def verify_login(self, username, password):
        """Verifica las credenciales de login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener todos los usuarios para verificar
            cursor.execute("SELECT username, password FROM client")
            users = cursor.fetchall()
            
            conn.close()
            
            # Verificar cada usuario
            for stored_username, stored_password in users:
                try:
                    # Verificar username
                    username_bytes = username.encode('utf-8')
                    if bcrypt.checkpw(username_bytes, stored_username):
                        # Verificar password
                        password_bytes = password.encode('utf-8')
                        if bcrypt.checkpw(password_bytes, stored_password):
                            return True, "¡Bienvenido! Has iniciado sesión correctamente."
                except:
                    continue
            
            return False, "El usuario o la contraseña no son correctos. Por favor, verifica tus datos e intenta nuevamente."
            
        except Exception as e:
            return False, f"Lo sentimos, hubo un problema al iniciar sesión. Por favor, intenta nuevamente." 