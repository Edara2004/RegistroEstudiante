import tkinter as tk
from tkinter import ttk, LabelFrame, Checkbutton, messagebox


class AppLogin(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class AppLogin
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

        # Clear Entries
        def clear_box():
            username_entry.delete(0, "")
            password_entry.delete(0, "")

        # Login frame
        frame_login = LabelFrame(self)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)
        frame_login.configure(pady=20, padx=10)

        # Title
        login_label = ttk.Label(frame_login, text="INGRESA AL SISTEMA", font=("Roboto", "12", "bold"))
        login_label.grid_configure(row=0, column=0, columnspan=3, pady=10)

        # User Widget
        username_label = ttk.Label(frame_login, text="Usuario")
        username_label.grid_configure(row=1, column=0, pady=10, padx=20)
        username_entry = ttk.Entry(frame_login)
        username_entry.grid_configure(row=1, column=1)

        # Show hide password
        def show_hide_password():
            if password_entry['show'] == '*':
                password_entry['show'] = ''
            else:
                password_entry['show'] = '*'

        # Password Widget
        password_label = ttk.Label(frame_login, text="Contraseña")
        password_label.grid_configure(row=2, column=0)
        password_entry = ttk.Entry(frame_login, show="*")
        password_entry.grid_configure(row=2, column=1)
        register_show_password = Checkbutton(frame_login, text="Mostrar", font=("Roboto", "10"),
                                             command=show_hide_password)
        register_show_password.grid_configure(row=2, column=2)

        # Show receive message
        def register_message_info():
            text_message_register = messagebox.showinfo(title="Pasos para el registro de usuario",
                                                        message="1. Rellenar todo el formulario\n"
                                                                "2. Deben coincidir las contraseñas\n"
                                                                "3. Colocar la clave admin de manera obligatoria")

        # button Enter & Register
        button_label_enter_login = ttk.Button(frame_login, text="Entrar")
        button_label_enter_login.grid_configure(row=3, column=0, columnspan=2, padx=1, pady=15)
        button_label_register_login = ttk.Button(frame_login, text="Registar",
                                                 command=lambda: (register_message_info(),
                                                                  controller.show_frame(RegisterUser), clear_box()))
        button_label_register_login.grid_configure(row=3, column=1, columnspan=2, padx=1, pady=15)

        frame_login.pack(expand=True)


class RegisterUser(tk.LabelFrame):

    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent)

        # Clear Entries
        def clear_box():
            register_id_entry_user.delete(0, "")
            register_entry_user.delete(0, "")
            password_entry.delete(0, "")
            password_entry_2.delete(0, "")
            register_admin_password_entry.delete(0, "")

        def check_box():

            # Entries List
            var = [register_id_entry_user.get(),
                   register_entry_user.get(),
                   password_entry.get(),
                   password_entry_2.get(),
                   register_admin_password_entry.get()]

            for var in var:
                if var != '':
                    True
                else:
                    return messagebox.showerror(title="Error", message="Ninguna casilla debe estar vacía.")


        # Setup frame
        frame_register = LabelFrame(self)
        frame_register.grid_rowconfigure(0, weight=1)
        frame_register.grid_columnconfigure(0, weight=1)
        frame_register.configure(pady=20, padx=10)

        # Title
        register_label = ttk.Label(frame_register, text="Registro de usuario", font=("Roboto", "14", "bold"))
        register_label.grid_configure(row=0, column=0, columnspan=3, pady=20)

        # ID widget
        register_id_user = ttk.Label(frame_register, text="Escribir ID", font=("Roboto", "10"))
        register_id_user.grid_configure(row=1, column=0, pady=5)
        register_id_entry_user = ttk.Entry(frame_register)
        register_id_entry_user.grid_configure(row=1, column=1, pady=5)

        # User widget
        register_label_user = ttk.Label(frame_register, text="Escribir Usuario", font=("Roboto", "10"))
        register_label_user.grid_configure(row=2, column=0)
        register_entry_user = ttk.Entry(frame_register)
        register_entry_user.grid_configure(row=2, column=1)

        # Password widget
        register_label_password = ttk.Label(frame_register, text="Escribir Contraseña", font=("Roboto", "10"))
        register_label_password.grid_configure(row=3, column=0, padx=5, pady=3)
        password_entry = ttk.Entry(frame_register, show="*", textvariable='')
        password_entry.grid_configure(row=3, column=1, padx=5, pady=3)
        register_label_password_2 = ttk.Label(frame_register, text="Confirmar Contraseña", font=("Roboto", "10"))
        register_label_password_2.grid_configure(row=4, column=0, padx=5, pady=3)
        password_entry_2 = ttk.Entry(frame_register, show="*")
        password_entry_2.grid_configure(row=4, column=1, padx=5, pady=3)

        # Admin Password
        register_label_admin_password = ttk.Label(frame_register, text="Contraseña Admin", font=("Roboto", "10"))
        register_label_admin_password.grid_configure(row=5, column=0, padx=5, pady=3)
        register_admin_password_entry = ttk.Entry(frame_register, show="*")
        register_admin_password_entry.grid_configure(row=5, column=1, padx=5, pady=3)
        register_admin_password_entry.delete(0, "")

        # Button register & Cancel
        register_button_users = ttk.Button(frame_register, text="Registrar", command=check_box)
        register_button_users.grid_configure(row=6, column=0, padx=3, pady=10)

        register_button_cancel = ttk.Button(frame_register, text="Cancelar",
                                            command=lambda: (controller.show_frame(LoginUser), clear_box()))
        register_button_cancel.grid_configure(row=6, column=1, padx=3, pady=10)

        frame_register.pack(expand=True)


root = AppLogin()
root.resizable(True, True)

# Run Mainloop
root.mainloop()
