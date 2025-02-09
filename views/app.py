import tkinter as tk
from tkinter import ttk, LabelFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("C.I.E by Eduar Rodriguez")
        self.geometry("1366x768")

        # Login frame
        frame_login = LabelFrame(self)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)
        frame_login.configure(pady=20, padx=10)

        login_label = ttk.Label(frame_login, text="INGRESA AL SISTEMA", font=("Roboto", "12", "bold"))
        login_label.grid_configure(row=0, column=0, columnspan=2)

        username_label = ttk.Label(frame_login, text="Usuario")
        username_label.grid_configure(row=1, column=0, pady=10, padx=20)

        username_entry = ttk.Entry(frame_login)
        username_entry.grid_configure(row=1, column=1)

        password_label = ttk.Label(frame_login, text="Contraseña")
        password_label.grid_configure(row=2, column=0)

        password_entry = ttk.Entry(frame_login, show="******")
        password_entry.grid_configure(row=2, column=1)

        buttom_label_enter_login = ttk.Button(frame_login, text="Entrar")
        buttom_label_enter_login.grid_configure(row=3, column=0, pady=15)

        buttom_label_register_login = ttk.Button(frame_login, text="Registar", command= RegisterUser.pack())
        buttom_label_register_login.grid_configure(row=3, column=1, pady=15)

        frame_login.pack(expand=True)


class RegisterUser(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

        frame_register = LabelFrame(self)
        frame_register.grid_rowconfigure(0, weight=1)
        frame_register.grid_columnconfigure(0, weight=1)
        frame_register.configure(pady=20, padx=10)

        register_label = ttk.Label(frame_register, text="dadad", font=("Roboto", "12", "bold"))
        register_label.grid_rowconfigure(row=0, column=0, columnspam=2)

        frame_register.pack(expand=True)


root = App()
root.resizable(True, True)

root.mainloop()
