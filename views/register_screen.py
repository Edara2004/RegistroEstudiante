import tkinter as tk
from tkinter import ttk, messagebox
from config.theme import *

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
                messagebox.showerror("Contraseñas diferentes", "Las contraseñas no coinciden. Por favor, asegúrate de escribir la misma contraseña en ambos campos.")
                return
            
            if len(password) < 6:
                messagebox.showerror("Contraseña muy corta", "La contraseña debe tener al menos 6 caracteres para mayor seguridad.")
                return
            
            # Intentar registrar usuario
            success, message = controller.db_manager.register_user(username, password, admin_password)
            
            if success:
                messagebox.showinfo("¡Registro exitoso!", message)
                clear_box()
                controller.show_frame(controller.LoginUser)
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
        register_label = ttk.Label(inner_frame, text="Registro de usuario", font=FONT_TITLE, background=SECONDARY_COLOR, foreground=ACCENT_COLOR)
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
        
        register_button_cancel = ttk.Button(inner_frame, text="Cancelar", style='Cancel.TButton',
                                            command=lambda: (controller.show_frame(controller.LoginUser), clear_box()))
        register_button_cancel.pack(pady=5, fill="x") 