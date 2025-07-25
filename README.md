# Sistema de Registro de Estudiantes (C.I.E)

Sistema de gestión de estudiantes desarrollado por Eduar Rodriguez con interfaz gráfica moderna, base de datos SQLite y arquitectura modular.

## 🚀 Características

- **Interfaz gráfica moderna** con Tkinter
- **Diseño responsive** que se adapta a diferentes tamaños de pantalla
- **Sistema de autenticación** seguro con encriptación bcrypt
- **Base de datos SQLite** para almacenamiento persistente
- **Validación de datos** en tiempo real
- **Arquitectura modular** para fácil mantenimiento
- **Interfaz intuitiva** y fácil de usar

## 📋 Requisitos

- Python 3.7 o superior
- Tkinter (incluido con Python)
- bcrypt
- sqlite3 (incluido con Python)

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install bcrypt
   ```

## 🎯 Uso

### Ejecutar la aplicación:
```bash
python app_main.py
```

### Funcionalidades:

#### 🔐 Sistema de Login
- **Usuario:** Ingresa tu nombre de usuario
- **Contraseña:** Ingresa tu contraseña
- **Mostrar:** Checkbox para mostrar/ocultar contraseña

#### 📝 Registro de Usuarios
- **ID:** Número de identificación (debe ser numérico)
- **Usuario:** Nombre de usuario único
- **Contraseña:** Mínimo 6 caracteres
- **Confirmar Contraseña:** Debe coincidir con la contraseña
- **Contraseña Admin:** Clave de administrador (por defecto: `admin123`)
- **Botones:** Registrar, Cancelar (limpia campos)

#### 🏠 Dashboard
- **Panel de control** con interfaz limpia
- **Descripción de funcionalidades** disponibles
- **Botón de cerrar sesión** con confirmación

## 🗄️ Base de Datos

La aplicación crea automáticamente las siguientes tablas:

### Tabla `client`
- `username`: Nombre de usuario (encriptado)
- `password`: Contraseña (encriptada)
- `secret_answer`: Respuesta secreta (encriptada)

### Tabla `students`
- `student_id`: ID del estudiante (clave primaria)
- `student_fullname`: Nombre completo
- `birthday`: Fecha de nacimiento
- `address`: Dirección
- `blood_type`: Tipo de sangre
- `phone_number`: Número de teléfono
- `date_of_entry`: Fecha de ingreso
- `gender`: Género
- `email`: Correo electrónico
- `nationality`: Nacionalidad

## 🔒 Seguridad

- **Encriptación bcrypt** para contraseñas y datos sensibles
- **Validación de entrada** para prevenir errores
- **Manejo de errores** robusto
- **Contraseñas seguras** con longitud mínima

## 🎨 Interfaz

### Paleta de Colores:
- **Primario:** #2E4053 (Azul oscuro)
- **Secundario:** #F2F4F4 (Gris claro)
- **Acento:** #2980B9 (Azul medio)
- **Éxito:** #27AE60 (Verde)
- **Cancelar:** #E74C3C (Rojo)

### Características de la UI:
- **Responsive:** Se adapta al tamaño de la ventana
- **Moderno:** Diseño limpio y profesional
- **Accesible:** Controles fáciles de usar
- **Consistente:** Estilo uniforme en toda la aplicación

## 🧪 Pruebas

Para verificar que todo funciona correctamente:
```bash
python test_app.py
```

## 📁 Estructura del Proyecto

```
RegistroEstudiante/
├── app_main.py              # Aplicación principal
├── config/
│   ├── __init__.py
│   └── theme.py             # Configuraciones y tema
├── database/
│   ├── __init__.py
│   ├── database.py          # Configuración de BD original
│   ├── db_manager.py        # Gestor de BD modular
│   ├── models.py            # Modelos de datos
│   └── queries.py           # Consultas SQL
├── utils/
│   ├── __init__.py
│   ├── function_time/
│   │   └── time_function.py
│   └── styles.py            # Configuración de estilos
├── views/
│   ├── __init__.py
│   ├── app.py               # Aplicación original
│   ├── login_screen.py      # Pantalla de login
│   ├── register_screen.py   # Pantalla de registro
│   └── dashboard_screen.py  # Pantalla del dashboard
├── model/
│   ├── course/
│   ├── reports/
│   └── users/
├── tests/
├── student_data.db          # Base de datos SQLite
├── test_app.py             # Archivo de prueba
└── README.md               # Este archivo
```

## 🔧 Configuración

### Cambiar contraseña de administrador:
Edita la línea en `config/theme.py`:
```python
ADMIN_PASSWORD = "admin123"  # Cambia "admin123" por tu contraseña
```

### Personalizar colores:
Modifica las constantes de color en `config/theme.py`:
```python
PRIMARY_COLOR = "#2E4053"
SECONDARY_COLOR = "#F2F4F4"
# ... etc
```

## 🆕 Nuevas Características

### Pantalla Completa:
- **Ejecución automática** en pantalla completa
- **Mejor aprovechamiento** del espacio disponible
- **Experiencia inmersiva** para el usuario

### Arquitectura Modular:
- **Separación de responsabilidades** en archivos específicos
- **Código más legible** y mantenible
- **Fácil extensión** de funcionalidades
- **Reutilización de componentes**

## 🐛 Solución de Problemas

### Error de importación:
```bash
pip install bcrypt
```

### Base de datos no se crea:
- Verifica permisos de escritura en el directorio
- La BD se crea automáticamente al ejecutar la app

### Problemas de interfaz:
- Asegúrate de tener Tkinter instalado
- En Linux: `sudo apt-get install python3-tk`

## 📝 Licencia

Este proyecto está bajo la licencia incluida en el archivo LICENSE.

## 👨‍💻 Autor

**Eduar Rodriguez** - Desarrollador del sistema C.I.E

---

¡Disfruta usando el Sistema de Registro de Estudiantes! 🎓
