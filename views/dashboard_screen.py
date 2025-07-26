import tkinter as tk
from tkinter import ttk, messagebox
from config.theme import *

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
        dashboard_label = ttk.Label(inner_frame, text="Panel de Control", font=FONT_TITLE, background=SECONDARY_COLOR, foreground=ACCENT_COLOR)
        dashboard_label.pack(pady=(0, 30))

        # Mensaje de bienvenida
        welcome_label = ttk.Label(inner_frame, text="¡Bienvenido al Sistema de Registro de Estudiantes!", 
                                 font=("Segoe UI", 14), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        welcome_label.pack(pady=(0, 20))

        # Descripción
        description_label = ttk.Label(inner_frame, text="Aquí puedes gestionar toda la información de los estudiantes.\n\n"
                                                       "Esta es tu área de trabajo principal donde podrás:\n"
                                                       "• Registrar nuevos estudiantes\n"
                                                       "• Ver y editar información existente\n"
                                                       "• Generar reportes\n"
                                                       "• Administrar el sistema", 
                                     font=("Segoe UI", 11), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR,
                                     justify="left")
        description_label.pack(pady=(0, 30))

        # Frame para botones de funcionalidades
        buttons_frame = tk.Frame(inner_frame, bg=SECONDARY_COLOR)
        buttons_frame.pack(fill="x", pady=(0, 20))

        # Botón Registrar Estudiante
        register_student_button = ttk.Button(buttons_frame, text="📝 Registrar Estudiante", 
                                            style='Success.TButton',
                                            command=lambda: controller.show_frame(controller.StudentEntryScreen))
        register_student_button.pack(pady=(0, 10), fill="x")

        # Botón Ver Estudiantes (placeholder para futura funcionalidad)
        view_students_button = ttk.Button(buttons_frame, text="👥 Ver Estudiantes", 
                                         style='Primary.TButton',
                                         command=lambda: controller.show_frame(controller.ShowStudentScreen))
        view_students_button.pack(pady=(0, 10), fill="x")

        # Botón Generar Reportes (placeholder para futura funcionalidad)
        reports_button = ttk.Button(buttons_frame, text="📊 Generar Reportes", 
                                   style='Primary.TButton',
                                   command=lambda: controller.show_frame(controller.ReportsScreen))
        reports_button.pack(pady=(0, 10), fill="x")

        # Botón de cerrar sesión
        def logout():
            response = messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")
            if response:
                controller.show_frame(controller.LoginUser)

        logout_button = ttk.Button(inner_frame, text="Cerrar Sesión", style='Cancel.TButton', command=logout)
        logout_button.pack(pady=(20, 0), fill="x") 