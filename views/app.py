import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test")

        set = ttk.Label(self, text="testing tkinter with poo", font=("Arial", "14", "bold"))
        set.pack(expand=True, fill="both")


root = App()
root.resizable(0, 0)

root.mainloop()
