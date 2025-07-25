#!/usr/bin/env python3
"""
Módulo de gestión de base de datos para el Sistema de Registro de Estudiantes (C.I.E)
Desarrollado por Eduar Rodriguez

Este módulo proporciona una interfaz robusta y segura para la gestión de la base de datos SQLite,
incluyendo creación de tablas, operaciones CRUD, y manejo de errores.
"""

import sqlite3
import os
import logging
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from datetime import datetime
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Excepción personalizada para errores de base de datos"""
    pass

class DatabaseManager:
    """
    Clase principal para la gestión de la base de datos del sistema de estudiantes.
    
    Esta clase proporciona métodos para:
    - Crear y gestionar la base de datos
    - Ejecutar operaciones CRUD
    - Manejar transacciones
    - Validar datos
    """
    
    def __init__(self, db_path: str = 'student_data.db'):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path (str): Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self._ensure_database_exists()
        logger.info(f"DatabaseManager inicializado con base de datos: {self.db_path}")
    
    def _ensure_database_exists(self) -> None:
        """Asegura que la base de datos y las tablas existan"""
        try:
            with self._get_connection() as conn:
                self._create_tables(conn)
                logger.info("Base de datos y tablas verificadas/creadas exitosamente")
        except Exception as e:
            logger.error(f"Error al crear/verificar la base de datos: {e}")
            raise DatabaseError(f"No se pudo inicializar la base de datos: {e}")
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager para obtener conexiones a la base de datos.
        
        Yields:
            sqlite3.Connection: Conexión a la base de datos
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Error de conexión a la base de datos: {e}")
            raise DatabaseError(f"Error de conexión: {e}")
        finally:
            if conn:
                conn.close()
    
    def _create_tables(self, conn: sqlite3.Connection) -> None:
        """
        Crea todas las tablas necesarias en la base de datos.
        
        Args:
            conn (sqlite3.Connection): Conexión a la base de datos
        """
        sql_statements = [
            # Tabla de usuarios del sistema
            """
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                secret_answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Tabla de estudiantes
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                student_fullname TEXT NOT NULL,
                birthday DATE NOT NULL,
                address TEXT NOT NULL,
                blood_type TEXT CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                phone_number TEXT,
                date_of_entry DATE NOT NULL,
                gender TEXT NOT NULL CHECK(gender IN ('Masculino', 'Femenino', 'Otro')),
                email TEXT UNIQUE,
                nationality TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Tabla de materias y calificaciones
            """
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                student_grades TEXT,
                student_notes TEXT,
                semester TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
            )
            """,
            
            # Tabla de relaciones familiares
            """
            CREATE TABLE IF NOT EXISTS student_relationship (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                related_person_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL CHECK(relationship_type IN ('Padre', 'Madre', 'Tutor', 'Hermano', 'Hermana', 'Otro')),
                fullname TEXT NOT NULL,
                person_photo BLOB,
                birthday DATE NOT NULL,
                blood_type TEXT CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                phone_number TEXT,
                job TEXT,
                address TEXT,
                marital_status TEXT NOT NULL CHECK(marital_status IN ('Soltero', 'Casado', 'Divorciado', 'Viudo')),
                nationality TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
            )
            """,
            
            # Tabla de reportes y ausencias
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                report_type TEXT NOT NULL CHECK(report_type IN ('Ausencia', 'Comportamiento', 'Académico', 'Otro')),
                absences INTEGER DEFAULT 0,
                reports_details TEXT,
                report_date DATE NOT NULL,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
            )
            """,
            
            # Tabla de auditoría
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES client (id)
            )
            """
        ]
        
        try:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()
            logger.info("Todas las tablas creadas/verificadas exitosamente")
        except sqlite3.Error as e:
            logger.error(f"Error al crear las tablas: {e}")
            raise DatabaseError(f"Error al crear las tablas: {e}")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT y retorna los resultados.
        
        Args:
            query (str): Consulta SQL
            params (tuple): Parámetros para la consulta
            
        Returns:
            List[Dict[str, Any]]: Lista de resultados como diccionarios
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            raise DatabaseError(f"Error en consulta: {e}")
    
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
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Error al ejecutar actualización: {e}")
            raise DatabaseError(f"Error en actualización: {e}")
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Obtiene información general de la base de datos.
        
        Returns:
            Dict[str, Any]: Información de la base de datos
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener información de tablas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # Obtener estadísticas de cada tabla
                stats = {}
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats[table] = count
                
                # Obtener información del archivo
                file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'database_path': self.db_path,
                    'file_size_bytes': file_size,
                    'file_size_mb': round(file_size / (1024 * 1024), 2),
                    'tables': tables,
                    'table_stats': stats,
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error al obtener información de la base de datos: {e}")
            raise DatabaseError(f"Error al obtener información: {e}")
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Crea una copia de seguridad de la base de datos.
        
        Args:
            backup_path (str): Ruta donde guardar el backup
            
        Returns:
            bool: True si el backup fue exitoso
        """
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Backup creado exitosamente en: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error al crear backup: {e}")
            return False
    
    def validate_data(self, table: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida los datos antes de insertarlos en la base de datos.
        
        Args:
            table (str): Nombre de la tabla
            data (Dict[str, Any]): Datos a validar
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        try:
            # Validaciones específicas por tabla
            if table == 'students':
                return self._validate_student_data(data)
            elif table == 'client':
                return self._validate_user_data(data)
            elif table == 'subjects':
                return self._validate_subject_data(data)
            else:
                return True, "Datos válidos"
        except Exception as e:
            logger.error(f"Error en validación de datos: {e}")
            return False, f"Error de validación: {e}"
    
    def _validate_student_data(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida datos de estudiantes"""
        required_fields = ['student_id', 'student_fullname', 'birthday', 'address', 'gender', 'nationality']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Campo requerido faltante: {field}"
        
        # Validar formato de fecha
        try:
            datetime.strptime(data['birthday'], '%Y-%m-%d')
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
        
        # Validar email si está presente
        if 'email' in data and data['email']:
            if '@' not in data['email'] or '.' not in data['email']:
                return False, "Formato de email inválido"
        
        return True, "Datos de estudiante válidos"
    
    def _validate_user_data(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida datos de usuarios"""
        required_fields = ['username', 'password']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Campo requerido faltante: {field}"
        
        if len(data['password']) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        return True, "Datos de usuario válidos"
    
    def _validate_subject_data(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida datos de materias"""
        required_fields = ['student_id', 'subject_name', 'semester', 'academic_year']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Campo requerido faltante: {field}"
        
        return True, "Datos de materia válidos"

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()

def initialize_database():
    """Función de inicialización para compatibilidad con código existente"""
    try:
        logger.info("Inicializando base de datos...")
        info = db_manager.get_database_info()
        logger.info(f"Base de datos inicializada: {info['tables']} tablas encontradas")
        return True
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar inicialización si se ejecuta directamente
    initialize_database()
