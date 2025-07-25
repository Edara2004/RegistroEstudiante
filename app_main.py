#!/usr/bin/env python3
"""
Aplicación principal del Sistema de Registro de Estudiantes (C.I.E)
Desarrollado por Eduar Rodriguez
"""

import tkinter as tk
from tkinter import ttk

# Importar configuraciones
from config.theme import *
from database.db_manager import DatabaseManager
from utils.styles import configure_styles

# Importar pantallas
from views.login_screen import LoginUser
from views.register_screen import RegisterUser
from views.dashboard_screen import Dashboard

class AppLogin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(APP_TITLE)
        
        # Configuración de pantalla completa
        self.state('zoomed')  # Pantalla completa en Windows
        self.configure(bg=PRIMARY_COLOR)
        
        # Hacer la ventana responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inicializar gestor de base de datos
        self.db_manager = DatabaseManager()

        # Configurar estilos
        configure_styles(self)

        # Contenedor principal responsive
        container = tk.Frame(self, bg=PRIMARY_COLOR)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inicializar frames
        self.frames = {}
        for F in (LoginUser, RegisterUser, Dashboard):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Almacenar referencias a las clases para navegación
        self.LoginUser = LoginUser
        self.RegisterUser = RegisterUser
        self.Dashboard = Dashboard

        self.show_frame(LoginUser)

    def show_frame(self, cont):
        """Muestra el frame especificado"""
        frame = self.frames[cont]
        frame.tkraise()

def main():
    """Función principal para ejecutar la aplicación"""
    root = AppLogin()
    root.resizable(True, True)
    root.mainloop()

if __name__ == "__main__":
    main() 