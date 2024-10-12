import tkinter as tk
from tkinter import ttk, Frame, Button, Label


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("C.I.E by Eduar Rodriguez")
        self.geometry("1366x768")

        # Login frame

        frame_login = Frame(self)
        frame_login.grid_rowconfigure(0, weight=1)
        frame_login.grid_columnconfigure(0, weight=1)

        login_label = ttk.Label(frame_login, text="Ingresar al sistema", font=("Roboto", "12", "bold"))
        login_label.pack(expand=True, fill="both")
        login_label.grid_configure(row=0, column=0)

        username_label = ttk.Label(frame_login, text="Usuario", font=("Roboto", "12", "bold"))
        username_label.grid_configure(row=1, column=0)
        username_label.pack(expand=True)

        username_entry = ttk.Entry(frame_login)
        username_entry.grid_configure(row=1, column=1)

        password_label = ttk.Label(frame_login, text="Contraseña")
        password_label.grid_configure(row=2, column=0)

        password_entry = ttk.Entry(frame_login, show="Contraseña")
        password_entry.grid_configure(row=2, column=1)

        frame_login.pack()


root = App()
root.resizable(False, False)

root.mainloop()
