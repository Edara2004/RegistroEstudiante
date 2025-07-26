import sqlite3
import bcrypt
import os
from typing import Dict, Any, List, Optional
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

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
        
        # Verificar y actualizar la estructura de la tabla students si es necesario
        self._update_students_table_structure(cursor)
        
        conn.commit()
        conn.close()

    def _update_students_table_structure(self, cursor):
        """Actualiza la estructura de la tabla students si es necesario"""
        try:
            # Obtener información de las columnas existentes
            cursor.execute("PRAGMA table_info(students)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Lista de columnas requeridas
            required_columns = {
                'student_id': 'INTEGER UNIQUE',
                'student_fullname': 'TEXT NOT NULL',
                'birthday': 'TEXT NOT NULL',
                'address': 'TEXT NOT NULL',
                'blood_type': 'TEXT',
                'phone_number': 'TEXT',
                'date_of_entry': 'TEXT',
                'gender': 'TEXT NOT NULL',
                'email': 'TEXT',
                'nationality': 'TEXT NOT NULL'
            }
            
            # Verificar si faltan columnas
            missing_columns = []
            for col_name, col_type in required_columns.items():
                if col_name not in columns:
                    missing_columns.append((col_name, col_type))
            
            # Agregar columnas faltantes
            for col_name, col_type in missing_columns:
                try:
                    cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
                    print(f"Columna '{col_name}' agregada a la tabla students")
                except Exception as e:
                    print(f"Error agregando columna '{col_name}': {e}")
                    
        except Exception as e:
            print(f"Error actualizando estructura de tabla students: {e}")
            # Si hay un error, recrear la tabla
            try:
                cursor.execute("DROP TABLE IF EXISTS students")
                cursor.execute("""
                    CREATE TABLE students (
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
                print("Tabla students recreada con la estructura correcta")
            except Exception as recreate_error:
                print(f"Error recreando tabla students: {recreate_error}")
    
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

    def insert_student(self, student_data: Dict[str, Any]) -> bool:
        """
        Inserta un nuevo estudiante en la base de datos.
        
        Args:
            student_data (Dict[str, Any]): Datos del estudiante
            
        Returns:
            bool: True si se insertó correctamente, False en caso contrario
        """
        try:
            # Validar datos antes de insertar
            is_valid, message = self.validate_data('students', student_data)
            if not is_valid:
                logger.error(f"Error de validación: {message}")
                return False
            
            # Preparar la consulta
            query = """
                INSERT INTO students (
                    student_id, student_fullname, birthday, address, blood_type,
                    phone_number, date_of_entry, gender, email, nationality
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                student_data['student_id'],
                student_data['student_fullname'],
                student_data['birthday'],
                student_data['address'],
                student_data['blood_type'],
                student_data['phone_number'],
                student_data['date_of_entry'],
                student_data['gender'],
                student_data['email'],
                student_data['nationality']
            )
            
            # Ejecutar la inserción
            rows_affected = self.execute_update(query, params)
            
            if rows_affected > 0:
                logger.info(f"Estudiante insertado exitosamente: ID {student_data['student_id']}")
                return True
            else:
                logger.error("No se pudo insertar el estudiante")
                return False
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Error de integridad al insertar estudiante: {e}")
            return False
        except Exception as e:
            logger.error(f"Error al insertar estudiante: {e}")
            return False 

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Ejecuta una consulta de actualización (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): Consulta SQL
            params (tuple): Parámetros para la consulta
            
        Returns:
            int: Número de filas afectadas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return 0

    def validate_data(self, table_name: str, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Valida los datos antes de insertar en la base de datos.
        
        Args:
            table_name (str): Nombre de la tabla
            data (Dict[str, Any]): Datos a validar
            
        Returns:
            tuple[bool, str]: (es_válido, mensaje_error)
        """
        try:
            if table_name == 'students':
                return self._validate_student_data(data)
            elif table_name == 'client':
                return self._validate_client_data(data)
            elif table_name == 'subjects':
                return self._validate_subject_data(data)
            else:
                return False, f"Tabla '{table_name}' no soportada para validación"
        except Exception as e:
            logger.error(f"Error en validación de datos: {e}")
            return False, f"Error de validación: {str(e)}"

    def _validate_student_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida datos específicos de estudiantes"""
        try:
            # Validar campos requeridos
            required_fields = ['student_id', 'student_fullname', 'birthday', 'address', 'gender', 'nationality']
            for field in required_fields:
                if field not in data or not data[field]:
                    return False, f"Campo requerido '{field}' está vacío o faltante"
            
            # Validar que student_id sea un número
            if not isinstance(data['student_id'], int):
                return False, "El ID del estudiante debe ser un número"
            
            # Validar formato de fecha de nacimiento
            try:
                from datetime import datetime
                datetime.strptime(data['birthday'], '%Y-%m-%d')
            except ValueError:
                return False, "La fecha de nacimiento debe tener el formato YYYY-MM-DD"
            
            # Validar género
            valid_genders = ['Masculino', 'Femenino', 'Otro']
            if data['gender'] not in valid_genders:
                return False, f"Género debe ser uno de: {', '.join(valid_genders)}"
            
            # Validar tipo de sangre si está presente
            if data.get('blood_type'):
                valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                if data['blood_type'] not in valid_blood_types:
                    return False, f"Tipo de sangre debe ser uno de: {', '.join(valid_blood_types)}"
            
            # Validar email si está presente
            if data.get('email'):
                if '@' not in data['email'] or '.' not in data['email']:
                    return False, "Formato de email inválido"
            
            return True, "Datos válidos"
            
        except Exception as e:
            return False, f"Error en validación de estudiante: {str(e)}"

    def _validate_client_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida datos específicos de clientes/usuarios"""
        try:
            required_fields = ['username', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return False, f"Campo requerido '{field}' está vacío o faltante"
            
            if len(data['password']) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            
            return True, "Datos válidos"
        except Exception as e:
            return False, f"Error en validación de cliente: {str(e)}"

    def _validate_subject_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Valida datos específicos de materias"""
        try:
            required_fields = ['student_id', 'subject_name']
            for field in required_fields:
                if field not in data or not data[field]:
                    return False, f"Campo requerido '{field}' está vacío o faltante"
            
            # Validar calificación si está presente
            if data.get('grade') is not None:
                grade = float(data['grade'])
                if grade < 0 or grade > 100:
                    return False, "La calificación debe estar entre 0 y 100"
            
            return True, "Datos válidos"
        except Exception as e:
            return False, f"Error en validación de materia: {str(e)}" 

    def get_all_students(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los estudiantes de la base de datos.
        
        Returns:
            List[Dict[str, Any]]: Lista de estudiantes con sus datos
        """
        try:
            query = """
                SELECT student_id, student_fullname, birthday, address, blood_type,
                       phone_number, date_of_entry, gender, email, nationality
                FROM students
                ORDER BY student_id
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                
                # Convertir a lista de diccionarios
                students = []
                for row in rows:
                    student = {
                        'student_id': row[0],
                        'student_fullname': row[1],
                        'birthday': row[2],
                        'address': row[3],
                        'blood_type': row[4],
                        'phone_number': row[5],
                        'date_of_entry': row[6],
                        'gender': row[7],
                        'email': row[8],
                        'nationality': row[9]
                    }
                    students.append(student)
                
                return students
                
        except Exception as e:
            logger.error(f"Error obteniendo estudiantes: {e}")
            return []

    def delete_student(self, student_id: int) -> bool:
        """
        Elimina un estudiante de la base de datos.
        
        Args:
            student_id (int): ID del estudiante a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            query = "DELETE FROM students WHERE student_id = ?"
            params = (student_id,)
            
            rows_affected = self.execute_update(query, params)
            
            if rows_affected > 0:
                logger.info(f"Estudiante eliminado exitosamente: ID {student_id}")
                return True
            else:
                logger.warning(f"No se encontró estudiante con ID {student_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando estudiante: {e}")
            return False

    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un estudiante específico por su ID.
        
        Args:
            student_id (int): ID del estudiante
            
        Returns:
            Optional[Dict[str, Any]]: Datos del estudiante o None si no se encuentra
        """
        try:
            query = """
                SELECT student_id, student_fullname, birthday, address, blood_type,
                       phone_number, date_of_entry, gender, email, nationality
                FROM students
                WHERE student_id = ?
            """
            params = (student_id,)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                
                if row:
                    return {
                        'student_id': row[0],
                        'student_fullname': row[1],
                        'birthday': row[2],
                        'address': row[3],
                        'blood_type': row[4],
                        'phone_number': row[5],
                        'date_of_entry': row[6],
                        'gender': row[7],
                        'email': row[8],
                        'nationality': row[9]
                    }
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Error obteniendo estudiante por ID: {e}")
            return None 

    @contextmanager
    def _get_connection(self):
        """Context manager para manejar conexiones a la base de datos"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close() 