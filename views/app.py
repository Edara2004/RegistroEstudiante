import tkinter as tk
from tkinter import ttk, LabelFrame, Checkbutton, messagebox
import sqlite3
import bcrypt
import os

# Paleta de colores y fuente base
PRIMARY_COLOR = "#2E4053"
SECONDARY_COLOR = "#F2F4F4"
ACCENT_COLOR = "#2980B9"
BUTTON_COLOR = "#3498DB"
BUTTON_HOVER = "#5DADE2"
BUTTON_ACTIVE = "#21618C"
SUCCESS_COLOR = "#27AE60"
SUCCESS_HOVER = "#58D68D"
CANCEL_COLOR = "#E74C3C"
CANCEL_HOVER = "#EC7063"
FONT_BASE = ("Segoe UI", 12)
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 11, "bold")


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
            # Verificar contraseña admin (puedes cambiar esto por la que necesites)
            if admin_password != "admin123":
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


class AppLogin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("C.I.E by Eduar Rodriguez")

        # Configuración responsive
        self.geometry("900x600")
        self.minsize(600, 400)  # Tamaño mínimo
        self.configure(bg=PRIMARY_COLOR)

        # Hacer la ventana responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inicializar gestor de base de datos
        self.db_manager = DatabaseManager()

        # Estilos ttk
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', background=SECONDARY_COLOR, foreground=PRIMARY_COLOR, font=FONT_LABEL)
        style.configure('TEntry', font=FONT_BASE)

        # Estilos personalizados para botones
        style.configure('Primary.TButton',
                        background=BUTTON_COLOR,
                        foreground='white',
                        font=FONT_BUTTON,
                        padding=(20, 10),
                        borderwidth=0,
                        focuscolor='none')
        style.map('Primary.TButton',
                  background=[('active', BUTTON_ACTIVE), ('pressed', BUTTON_ACTIVE)])

        style.configure('Success.TButton',
                        background=SUCCESS_COLOR,
                        foreground='white',
                        font=FONT_BUTTON,
                        padding=(20, 10),
                        borderwidth=0,
                        focuscolor='none')
        style.map('Success.TButton',
                  background=[('active', SUCCESS_HOVER), ('pressed', SUCCESS_HOVER)])

        style.configure('Cancel.TButton',
                        background=CANCEL_COLOR,
                        foreground='white',
                        font=FONT_BUTTON,
                        padding=(20, 10),
                        borderwidth=0,
                        focuscolor='none')
        style.map('Cancel.TButton',
                  background=[('active', CANCEL_HOVER), ('pressed', CANCEL_HOVER)])

        # Contenedor principal responsive
        container = tk.Frame(self, bg=PRIMARY_COLOR)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginUser, RegisterUser, Dashboard):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginUser)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)

        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def clear_box():
            username_entry.delete(0, "")
            password_entry.delete(0, "")

        def login():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Campos incompletos", "Por favor, completa todos los campos antes de continuar.")
                return

            success, message = controller.db_manager.verify_login(username, password)
            if success:
                messagebox.showinfo("¡Bienvenido!", message)
                clear_box()
                controller.show_frame(Dashboard)
            else:
                messagebox.showerror("Error de acceso", message)

        # Frame de login responsive
        frame_login = tk.Frame(self, bg=SECONDARY_COLOR, bd=2, relief="groove")
        frame_login.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # Configurar grid del frame de login
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)

        # Contenedor interno para centrar contenido
        inner_frame = tk.Frame(frame_login, bg=SECONDARY_COLOR)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        # Título
        login_label = ttk.Label(inner_frame, text="INGRESA AL SISTEMA", font=FONT_TITLE, background=SECONDARY_COLOR,
                                foreground=ACCENT_COLOR)
        login_label.pack(pady=(0, 20))

        # Usuario
        username_label = ttk.Label(inner_frame, text="Usuario:", font=FONT_LABEL)
        username_label.pack(anchor="w", pady=(10, 0))
        username_entry = ttk.Entry(inner_frame, width=30)
        username_entry.pack(fill="x", pady=5)

        # Mostrar/ocultar contraseña
        def show_hide_password():
            if password_entry['show'] == '*':
                password_entry['show'] = ''
            else:
                password_entry['show'] = '*'

        # Contraseña
        password_label = ttk.Label(inner_frame, text="Contraseña:", font=FONT_LABEL)
        password_label.pack(anchor="w", pady=(10, 0))
        password_entry = ttk.Entry(inner_frame, show="*", width=30)
        password_entry.pack(fill="x", pady=5)
        register_show_password = Checkbutton(inner_frame, text="Mostrar", font=("Segoe UI", 9),
                                             command=show_hide_password, bg=SECONDARY_COLOR,
                                             activebackground=SECONDARY_COLOR)
        register_show_password.pack(anchor="w", pady=(0, 10))

        # Mensaje de registro
        def register_message_info():
            text_message_register = messagebox.showinfo(title="Guía de registro",
                                                        message="¡Bienvenido al registro! 📝\n\n"
                                                                "Para crear tu cuenta, sigue estos pasos:\n\n"
                                                                "1️⃣ Completa todos los campos del formulario\n"
                                                                "2️⃣ El ID debe ser un número (ej: 12345)\n"
                                                                "3️⃣ La contraseña debe tener al menos 6 caracteres\n"
                                                                "4️⃣ Usa 'admin123' como contraseña de administrador\n"
                                                                "5️⃣ El ID será tu identificación personal\n\n"
                                                                "¡Es fácil y rápido! 🚀")
            return text_message_register

        # Botones
        button_label_enter_login = ttk.Button(inner_frame, text="Entrar", style='Primary.TButton', command=login)
        button_label_enter_login.pack(pady=(15, 5), fill="x")
        button_label_register_login = ttk.Button(inner_frame, text="Registrar", style='Success.TButton',
                                                 command=lambda: (register_message_info(),
                                                                  controller.show_frame(RegisterUser), clear_box()))
        button_label_register_login.pack(pady=5, fill="x")


class RegisterUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)

        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        def clear_box():
            register_id_entry_user.delete(0, "")
            register_entry_user.delete(0, "")
            password_entry.delete(0, "")
            password_entry_2.delete(0, "")
            register_admin_password_entry.delete(0, "")

        def check_box():
            # Obtener valores de los campos
            user_id = register_id_entry_user.get()
            username = register_entry_user.get()
            password = password_entry.get()
            password_confirm = password_entry_2.get()
            admin_password = register_admin_password_entry.get()

            # Validaciones
            if not all([user_id, username, password, password_confirm, admin_password]):
                messagebox.showerror("Información incompleta", "Por favor, completa todos los campos del formulario.")
                return

            if not user_id.isdigit():
                messagebox.showerror("ID inválido", "El ID debe ser un número. Por favor, ingresa solo números.")
                return

            if password != password_confirm:
                messagebox.showerror("Contraseñas diferentes",
                                     "Las contraseñas no coinciden. Por favor, asegúrate de escribir la misma contraseña en ambos campos.")
                return

            if len(password) < 6:
                messagebox.showerror("Contraseña muy corta",
                                     "La contraseña debe tener al menos 6 caracteres para mayor seguridad.")
                return

            # Intentar registrar usuario
            success, message = controller.db_manager.register_user(username, password, admin_password)

            if success:
                messagebox.showinfo("¡Registro exitoso!", message)
                clear_box()
                controller.show_frame(LoginUser)
            else:
                messagebox.showerror("Error en el registro", message)

        # Frame de registro responsive
        frame_register = tk.Frame(self, bg=SECONDARY_COLOR, bd=2, relief="groove")
        frame_register.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Configurar grid del frame de registro
        frame_register.grid_rowconfigure(0, weight=1)
        frame_register.grid_columnconfigure(0, weight=1)

        # Contenedor interno para centrar contenido
        inner_frame = tk.Frame(frame_register, bg=SECONDARY_COLOR)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Título
        register_label = ttk.Label(inner_frame, text="Registro de usuario", font=FONT_TITLE, background=SECONDARY_COLOR,
                                   foreground=ACCENT_COLOR)
        register_label.pack(pady=(0, 20))

        # ID
        register_id_user = ttk.Label(inner_frame, text="Escribir ID:", font=FONT_LABEL)
        register_id_user.pack(anchor="w", pady=(10, 0))
        register_id_entry_user = ttk.Entry(inner_frame, width=35)
        register_id_entry_user.pack(fill="x", pady=5)

        # Usuario
        register_label_user = ttk.Label(inner_frame, text="Escribir Usuario:", font=FONT_LABEL)
        register_label_user.pack(anchor="w", pady=(15, 0))
        register_entry_user = ttk.Entry(inner_frame, width=35)
        register_entry_user.pack(fill="x", pady=5)

        # Contraseña
        register_label_password = ttk.Label(inner_frame, text="Escribir Contraseña:", font=FONT_LABEL)
        register_label_password.pack(anchor="w", pady=(15, 0))
        password_entry = ttk.Entry(inner_frame, show="*", width=35)
        password_entry.pack(fill="x", pady=5)

        register_label_password_2 = ttk.Label(inner_frame, text="Confirmar Contraseña:", font=FONT_LABEL)
        register_label_password_2.pack(anchor="w", pady=(15, 0))
        password_entry_2 = ttk.Entry(inner_frame, show="*", width=35)
        password_entry_2.pack(fill="x", pady=5)

        # Contraseña admin
        register_label_admin_password = ttk.Label(inner_frame, text="Contraseña Admin:", font=FONT_LABEL)
        register_label_admin_password.pack(anchor="w", pady=(15, 0))
        register_admin_password_entry = ttk.Entry(inner_frame, show="*", width=35)
        register_admin_password_entry.pack(fill="x", pady=5)

        # Espacio adicional antes de los botones
        tk.Frame(inner_frame, height=20, bg=SECONDARY_COLOR).pack()

        # Botones
        register_button_users = ttk.Button(inner_frame, text="Registrar", style='Success.TButton', command=check_box)
        register_button_users.pack(pady=(10, 5), fill="x")

        # Botón regresar (sin limpiar campos)
        register_button_back = ttk.Button(inner_frame, text="Regresar", style='Primary.TButton',
                                          command=lambda: controller.show_frame(LoginUser))
        register_button_back.pack(pady=5, fill="x")

        register_button_cancel = ttk.Button(inner_frame, text="Cancelar", style='Cancel.TButton',
                                            command=lambda: (controller.show_frame(LoginUser), clear_box()))
        register_button_cancel.pack(pady=5, fill="x")


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)

        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame principal del dashboard
        dashboard_frame = tk.Frame(self, bg=SECONDARY_COLOR, bd=2, relief="groove")
        dashboard_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame del dashboard
        dashboard_frame.grid_rowconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(0, weight=1)

        # Contenedor interno
        inner_frame = tk.Frame(dashboard_frame, bg=SECONDARY_COLOR)
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        # Título del dashboard
        dashboard_label = ttk.Label(inner_frame, text="Panel de Control", font=FONT_TITLE, background=SECONDARY_COLOR,
                                    foreground=ACCENT_COLOR)
        dashboard_label.pack(pady=(0, 30))

        # Mensaje de bienvenida
        welcome_label = ttk.Label(inner_frame, text="¡Bienvenido al Sistema de Registro de Estudiantes!",
                                  font=("Segoe UI", 14), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        welcome_label.pack(pady=(0, 20))

        # Descripción
        description_label = ttk.Label(inner_frame,
                                      text="Aquí puedes gestionar toda la información de los estudiantes.\n\n"
                                           "Esta es tu área de trabajo principal donde podrás:\n"
                                           "• Registrar nuevos estudiantes\n"
                                           "• Ver y editar información existente\n"
                                           "• Generar reportes\n"
                                           "• Administrar el sistema",
                                      font=("Segoe UI", 11), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR,
                                      justify="left")
        description_label.pack(pady=(0, 30))

        # Botón de cerrar sesión
        def logout():
            response = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")
            if response:
                controller.show_frame(LoginUser)

        logout_button = ttk.Button(inner_frame, text="Cerrar Sesión", style='Cancel.TButton', command=logout)
        logout_button.pack(pady=(20, 0), fill="x")


root = AppLogin()
root.resizable(True, True)  # Permitir cambiar tamaño
root.mainloop()
