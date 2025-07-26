import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config.theme import *


class StudentEntryScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)

        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Variables para los campos
        self.student_id_var = tk.StringVar()
        self.fullname_var = tk.StringVar()
        self.birthday_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.blood_type_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.date_entry_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.nationality_var = tk.StringVar()

        # Configurar fecha actual para date_of_entry
        self.date_entry_var.set(datetime.now().strftime('%Y-%m-%d'))

        self._create_widgets(controller)

    def _create_widgets(self, controller):
        """Crea todos los widgets de la interfaz"""

        # Frame principal
        main_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        form_frame.grid_rowconfigure(1, weight=1)  # La fila del contenido
        form_frame.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ttk.Label(form_frame, text="Registro de Estudiante",
                                font=FONT_TITLE, background=SECONDARY_COLOR, foreground=ACCENT_COLOR)
        title_label.grid(row=0, column=0, pady=(20, 10))

        # Contenedor principal para los campos (2 columnas)
        content_frame = tk.Frame(form_frame, bg=SECONDARY_COLOR)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # Columna izquierda
        left_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.grid_columnconfigure(0, weight=1)

        # Columna derecha
        right_frame = tk.Frame(content_frame, bg=SECONDARY_COLOR)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        right_frame.grid_columnconfigure(0, weight=1)

        # Crear campos en columnas
        self._create_field(left_frame, "ID del Estudiante:", self.student_id_var, 0, required=True)
        self._create_field(left_frame, "Nombre Completo:", self.fullname_var, 1, required=True)
        self._create_field(left_frame, "Fecha de Nacimiento:", self.birthday_var, 2, required=True,
                           placeholder="YYYY-MM-DD")
        self._create_field(left_frame, "Dirección:", self.address_var, 3, required=True)
        self._create_field(left_frame, "Teléfono:", self.phone_var, 4, required=False)

        # Campo de tipo de sangre con combobox
        self._create_blood_type_field(right_frame, 0)

        # Campo de género con combobox
        self._create_gender_field(right_frame, 1)

        self._create_field(right_frame, "Email:", self.email_var, 2, required=False)
        self._create_field(right_frame, "Nacionalidad:", self.nationality_var, 3, required=True)
        self._create_field(right_frame, "Fecha de Ingreso:", self.date_entry_var, 4, required=True, readonly=True)

        # Botones en la parte inferior
        button_frame = tk.Frame(form_frame, bg=SECONDARY_COLOR)
        button_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # Botón Guardar
        save_button = ttk.Button(button_frame, text="💾 Guardar",
                                 style='Success.TButton', command=lambda: self._save_student(controller))
        save_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Botón Limpiar
        clear_button = ttk.Button(button_frame, text="🧹 Limpiar",
                                  style='Primary.TButton', command=self._clear_form)
        clear_button.grid(row=0, column=1, padx=5, sticky="ew")

        # Botón Volver
        back_button = ttk.Button(button_frame, text="⬅️ Volver",
                                 style='Cancel.TButton', command=lambda: controller.show_frame(controller.Dashboard))
        back_button.grid(row=0, column=2, padx=(10, 0), sticky="ew")

    def _create_field(self, parent, label_text, variable, row, required=False, readonly=False, placeholder=""):
        """Crea un campo de entrada con su etiqueta"""
        # Frame para el campo
        field_frame = tk.Frame(parent, bg=SECONDARY_COLOR)
        field_frame.grid(row=row, column=0, sticky="ew", pady=3)
        field_frame.grid_columnconfigure(0, weight=1)

        # Etiqueta
        label = ttk.Label(field_frame, text=label_text, font=FONT_LABEL,
                          background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        label.grid(row=0, column=0, sticky="w", pady=(2, 0))

        # Campo de entrada
        if readonly:
            entry = ttk.Entry(field_frame, textvariable=variable, state="readonly")
        else:
            entry = ttk.Entry(field_frame, textvariable=variable)
        entry.grid(row=1, column=0, sticky="ew", pady=1)

        # Indicador de campo requerido
        if required:
            required_label = ttk.Label(field_frame, text="*", font=("Segoe UI", 10, "bold"),
                                       background=SECONDARY_COLOR, foreground=CANCEL_COLOR)
            required_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

    def _create_blood_type_field(self, parent, row):
        """Crea el campo de tipo de sangre con combobox"""
        field_frame = tk.Frame(parent, bg=SECONDARY_COLOR)
        field_frame.grid(row=row, column=0, sticky="ew", pady=3)
        field_frame.grid_columnconfigure(0, weight=1)

        label = ttk.Label(field_frame, text="Tipo de Sangre:", font=FONT_LABEL,
                          background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        label.grid(row=0, column=0, sticky="w", pady=(2, 0))

        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        blood_combo = ttk.Combobox(field_frame, textvariable=self.blood_type_var,
                                   values=blood_types, state="readonly")
        blood_combo.grid(row=1, column=0, sticky="ew", pady=1)

    def _create_gender_field(self, parent, row):
        """Crea el campo de género con combobox"""
        field_frame = tk.Frame(parent, bg=SECONDARY_COLOR)
        field_frame.grid(row=row, column=0, sticky="ew", pady=3)
        field_frame.grid_columnconfigure(0, weight=1)

        label = ttk.Label(field_frame, text="Género:", font=FONT_LABEL,
                          background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        label.grid(row=0, column=0, sticky="w", pady=(2, 0))

        genders = ['Masculino', 'Femenino']
        gender_combo = ttk.Combobox(field_frame, textvariable=self.gender_var,
                                    values=genders, state="readonly")
        gender_combo.grid(row=1, column=0, sticky="ew", pady=1)

        # Indicador de campo requerido
        required_label = ttk.Label(field_frame, text="*", font=("Segoe UI", 10, "bold"),
                                   background=SECONDARY_COLOR, foreground=CANCEL_COLOR)
        required_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

    def _validate_data(self):
        """Valida todos los datos del formulario"""
        errors = []

        # Validar campos requeridos
        if not self.student_id_var.get().strip():
            errors.append("El ID del estudiante es obligatorio")
        elif not self.student_id_var.get().isdigit():
            errors.append("El ID del estudiante debe ser un número")

        if not self.fullname_var.get().strip():
            errors.append("El nombre completo es obligatorio")

        if not self.birthday_var.get().strip():
            errors.append("La fecha de nacimiento es obligatoria")
        else:
            try:
                datetime.strptime(self.birthday_var.get(), '%Y-%m-%d')
            except ValueError:
                errors.append("La fecha de nacimiento debe tener el formato YYYY-MM-DD")

        if not self.address_var.get().strip():
            errors.append("La dirección es obligatoria")

        if not self.gender_var.get():
            errors.append("El género es obligatorio")

        if not self.nationality_var.get().strip():
            errors.append("La nacionalidad es obligatoria")

        # Validar email si está presente
        if self.email_var.get().strip():
            if '@' not in self.email_var.get() or '.' not in self.email_var.get():
                errors.append("El formato del email no es válido")

        return errors

    def _save_student(self, controller):
        """Guarda el estudiante en la base de datos"""
        # Validar datos
        errors = self._validate_data()
        if errors:
            error_message = "Por favor, corrige los siguientes errores:\n\n" + "\n".join(
                f"• {error}" for error in errors)
            messagebox.showerror("Errores de Validación", error_message)
            return

        try:
            # Preparar datos
            student_data = {
                'student_id': int(self.student_id_var.get()),
                'student_fullname': self.fullname_var.get().strip(),
                'birthday': self.birthday_var.get(),
                'address': self.address_var.get().strip(),
                'blood_type': self.blood_type_var.get() if self.blood_type_var.get() else None,
                'phone_number': self.phone_var.get().strip() if self.phone_var.get().strip() else None,
                'date_of_entry': self.date_entry_var.get(),
                'gender': self.gender_var.get(),
                'email': self.email_var.get().strip() if self.email_var.get().strip() else None,
                'nationality': self.nationality_var.get().strip()
            }

            # Insertar en la base de datos
            success = controller.db_manager.insert_student(student_data)

            if success:
                messagebox.showinfo("Éxito", "¡Estudiante registrado exitosamente!")
                self._clear_form()
            else:
                messagebox.showerror("Error",
                                     "No se pudo registrar el estudiante. Verifica que el ID no esté duplicado.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el estudiante: {str(e)}")

    def _clear_form(self):
        """Limpia todos los campos del formulario"""
        self.student_id_var.set("")
        self.fullname_var.set("")
        self.birthday_var.set("")
        self.address_var.set("")
        self.blood_type_var.set("")
        self.phone_var.set("")
        self.date_entry_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.gender_var.set("")
        self.email_var.set("")
        self.nationality_var.set("")
