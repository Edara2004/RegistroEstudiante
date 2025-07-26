import tkinter as tk
from tkinter import ttk, Checkbutton, messagebox
from config.theme import *


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
                controller.show_frame(controller.Dashboard)
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
                                                                  controller.show_frame(controller.RegisterUser),
                                                                  clear_box()))
        button_label_register_login.pack(pady=5, fill="x")
