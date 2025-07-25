from tkinter import ttk
from config.theme import *

def configure_styles(root):
    """Configura todos los estilos de la aplicación"""
    style = ttk.Style(root)
    style.theme_use('clam')
    
    # Estilos básicos
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