import tkinter as tk
from tkinter import ttk, LabelFrame


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class App
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("C.I.E by Eduar Rodriguez")
        self.geometry("1366x768")

        # Creating a container
        container = tk.LabelFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing frames to an empty array
        self.frames = {}

        # Iterating through a tuple consisting of the different page layouts
        for F in (LoginUser, RegisterUser):
            frame = F(container, self)

            # Initializing frame of that object from LoginUser, Register respectively with for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginUser)

    # To display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginUser(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent)

        # Login frame
        frame_login = LabelFrame(self)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)
        frame_login.configure(pady=20, padx=10)

        # Title
        login_label = ttk.Label(frame_login, text="INGRESA AL SISTEMA", font=("Roboto", "12", "bold"))
        login_label.grid_configure(row=0, column=0, columnspan=2)

        # User Widget
        username_label = ttk.Label(frame_login, text="Usuario")
        username_label.grid_configure(row=1, column=0, pady=10, padx=20)
        username_entry = ttk.Entry(frame_login)
        username_entry.grid_configure(row=1, column=1)

        # Password Widget
        password_label = ttk.Label(frame_login, text="Contraseña")
        password_label.grid_configure(row=2, column=0)
        password_entry = ttk.Entry(frame_login, show="******")
        password_entry.grid_configure(row=2, column=1)

        # Buttom Enter & Register
        buttom_label_enter_login = ttk.Button(frame_login, text="Entrar")
        buttom_label_enter_login.grid_configure(row=3, column=0, padx=15, pady=15)
        buttom_label_register_login = ttk.Button(frame_login, text="Registar",
                                                 command=lambda: controller.show_frame(RegisterUser))
        buttom_label_register_login.grid_configure(row=3, column=1, padx=15, pady=15)

        frame_login.pack(expand=True)


class RegisterUser(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent)

        # Setup frame
        frame_register = LabelFrame(self)
        frame_register.grid_rowconfigure(0, weight=1)
        frame_register.grid_columnconfigure(0, weight=1)
        frame_register.configure(pady=20, padx=10)

        # Title
        register_label = ttk.Label(frame_register, text="Registro de usuario", font=("Roboto", "14", "bold"))
        register_label.grid_configure(row=0, column=0, columnspan=2, pady=20)

        # User widget
        register_label_user = ttk.Label(frame_register, text="Escribir Usuario", font=("Roboto", "10"))
        register_label_user.grid_configure(row=1, column=0)
        register_entry_user = ttk.Entry(frame_register)
        register_entry_user.grid_configure(row=1, column=1)

        # Password widget
        register_label_password = ttk.Label(frame_register, text="Escribir Contraseña", font=("Roboto", "10"))
        register_label_password.grid_configure(row=2, column=0, padx=5, pady=3)
        register_entry_password = ttk.Entry(frame_register)
        register_entry_password.grid_configure(row=2, column=1, padx=5, pady=3)
        register_label_password_2 = ttk.Label(frame_register, text="Confirmar Contraseña", font=("Roboto", "10"))
        register_label_password_2.grid_configure(row=3, column=0, padx=5, pady=3)
        register_entry_password_2 = ttk.Entry(frame_register)
        register_entry_password_2.grid_configure(row=3, column=1, padx=5, pady=3)

        # Admin Password
        register_label_admin_password = ttk.Label(frame_register, text="Contraseña Admin", font=("Roboto", "10"))
        register_label_admin_password.grid_configure(row=4, column=0, padx=5, pady=3)
        register_admin_password_entry = ttk.Entry(frame_register)
        register_admin_password_entry.grid_configure(row=4, column=1, padx=5, pady=3)

        # Buttom register & Cancel
        register_buttom_users = ttk.Button(frame_register, text="Registrar")
        register_buttom_users.grid_configure(row=5, column=0, padx=3, pady=10)
        register_buttom_cancel = ttk.Button(frame_register, text="Cancelar",
                                            command=lambda: controller.show_frame(LoginUser))
        register_buttom_cancel.grid_configure(row=5, column=1, padx=3, pady=10)

        frame_register.pack(expand=True)


root = App()
root.resizable(True, True)

# Run Mainloop
root.mainloop()
