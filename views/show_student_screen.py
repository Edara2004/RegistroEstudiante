import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config.theme import *


class ShowStudentScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)

        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Variables
        self.controller = controller
        self.students_data = []
        self.filtered_data = []

        # Crear widgets
        self._create_widgets()

        # Cargar datos iniciales
        self._load_students()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""

        # Frame principal
        main_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)  # La tabla ocupará el espacio
        main_frame.grid_columnconfigure(0, weight=1)

        # Frame del título
        title_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title_frame.grid_columnconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(title_frame, text="📚 Gestión de Estudiantes",
                                font=FONT_TITLE, background=SECONDARY_COLOR, foreground=ACCENT_COLOR)
        title_label.grid(row=0, column=0, padx=20, pady=15)

        # Contador de estudiantes
        self.count_label = ttk.Label(title_frame, text="Total: 0 estudiantes",
                                     font=("Segoe UI", 11), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        self.count_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(1, weight=1)

        # Frame de búsqueda
        search_frame = tk.Frame(controls_frame, bg=SECONDARY_COLOR)
        search_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Etiqueta de búsqueda
        search_label = ttk.Label(search_frame, text="🔍 Buscar:", font=FONT_LABEL,
                                 background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        search_label.pack(side="left", padx=(0, 10))

        # Campo de búsqueda
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._filter_students)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(0, 10))

        # Botón limpiar búsqueda
        clear_search_btn = ttk.Button(search_frame, text="🗑️ Limpiar",
                                      style='Cancel.TButton', command=self._clear_search)
        clear_search_btn.pack(side="left")

        # Frame de botones de acción
        actions_frame = tk.Frame(controls_frame, bg=SECONDARY_COLOR)
        actions_frame.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Botón actualizar
        refresh_btn = ttk.Button(actions_frame, text="🔄 Actualizar",
                                 style='Primary.TButton', command=self._load_students)
        refresh_btn.pack(side="right", padx=(5, 0))

        # Botón agregar nuevo
        add_btn = ttk.Button(actions_frame, text="➕ Agregar",
                             style='Success.TButton',
                             command=lambda: self.controller.show_frame(self.controller.StudentEntryScreen))
        add_btn.pack(side="right", padx=(5, 0))

        # Frame de la tabla
        table_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        table_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Crear Treeview (tabla)
        self._create_table(table_frame)

        # Frame de botones inferiores
        bottom_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        bottom_frame.grid(row=3, column=0, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        # Botón editar
        edit_btn = ttk.Button(bottom_frame, text="✏️ Editar",
                              style='Primary.TButton', command=self._edit_student)
        edit_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        # Botón eliminar
        delete_btn = ttk.Button(bottom_frame, text="🗑️ Eliminar",
                                style='Cancel.TButton', command=self._delete_student)
        delete_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        # Botón volver
        back_btn = ttk.Button(bottom_frame, text="⬅️ Volver al Dashboard",
                              style='Cancel.TButton',
                              command=lambda: self.controller.show_frame(self.controller.Dashboard))
        back_btn.grid(row=0, column=2, padx=10, pady=15, sticky="ew")

    def _create_table(self, parent):
        """Crea la tabla de estudiantes"""

        # Frame para la tabla con scrollbar
        table_container = tk.Frame(parent, bg=SECONDARY_COLOR)
        table_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        columns = ('ID', 'Nombre', 'Género', 'Edad', 'Teléfono', 'Email', 'Nacionalidad', 'Fecha Ingreso')

        self.tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15)

        # Configurar columnas
        column_widths = {
            'ID': 80,
            'Nombre': 200,
            'Género': 100,
            'Edad': 60,
            'Teléfono': 120,
            'Email': 180,
            'Nacionalidad': 120,
            'Fecha Ingreso': 120
        }

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_table(c))
            self.tree.column(col, width=column_widths[col], minwidth=50)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid de la tabla y scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

    def _load_students(self):
        """Carga los estudiantes desde la base de datos"""
        try:
            # Obtener datos de la base de datos
            self.students_data = self.controller.db_manager.get_all_students()
            self.filtered_data = self.students_data.copy()

            # Actualizar tabla
            self._update_table()

            # Actualizar contador
            self.count_label.config(text=f"Total: {len(self.students_data)} estudiantes")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")

    def _update_table(self):
        """Actualiza la tabla con los datos filtrados"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar datos filtrados
        for student in self.filtered_data:
            # Calcular edad
            age = self._calculate_age(student.get('birthday', ''))

            # Preparar datos para la tabla
            values = (
                student.get('student_id', ''),
                student.get('student_fullname', ''),
                student.get('gender', ''),
                age,
                student.get('phone_number', '') or 'N/A',
                student.get('email', '') or 'N/A',
                student.get('nationality', ''),
                student.get('date_of_entry', '')
            )

            self.tree.insert('', 'end', values=values)

    def _calculate_age(self, birthday_str):
        """Calcula la edad basada en la fecha de nacimiento"""
        if not birthday_str:
            return 'N/A'

        try:
            birth_date = datetime.strptime(birthday_str, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return str(age)
        except:
            return 'N/A'

    def _filter_students(self, *args):
        """Filtra los estudiantes basado en la búsqueda"""
        search_term = self.search_var.get().lower()

        if not search_term:
            self.filtered_data = self.students_data.copy()
        else:
            self.filtered_data = []
            for student in self.students_data:
                # Buscar en múltiples campos
                searchable_fields = [
                    str(student.get('student_id', '')),
                    student.get('student_fullname', '').lower(),
                    student.get('gender', '').lower(),
                    student.get('phone_number', '').lower(),
                    student.get('email', '').lower(),
                    student.get('nationality', '').lower()
                ]

                if any(search_term in field for field in searchable_fields):
                    self.filtered_data.append(student)

        self._update_table()
        self.count_label.config(text=f"Mostrando: {len(self.filtered_data)} de {len(self.students_data)} estudiantes")

    def _clear_search(self):
        """Limpia la búsqueda"""
        self.search_var.set("")
        self.filtered_data = self.students_data.copy()
        self._update_table()
        self.count_label.config(text=f"Total: {len(self.students_data)} estudiantes")

    def _sort_table(self, column):
        """Ordena la tabla por la columna seleccionada"""
        # Obtener todos los elementos
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]

        # Ordenar
        items.sort()

        # Reorganizar elementos en la tabla
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)

    def _get_selected_student(self):
        """Obtiene el estudiante seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un estudiante.")
            return None

        # Obtener el ID del estudiante seleccionado
        student_id = self.tree.item(selection[0])['values'][0]

        # Buscar el estudiante en los datos
        for student in self.students_data:
            if student.get('student_id') == student_id:
                return student

        return None

    def _edit_student(self):
        """Edita el estudiante seleccionado"""
        student = self._get_selected_student()
        if student:
            # Por ahora mostrar un mensaje (se implementará la edición después)
            messagebox.showinfo("Editar Estudiante",
                                f"Funcionalidad de edición para: {student.get('student_fullname')}\n\n"
                                "Esta funcionalidad se implementará próximamente.")

    def _delete_student(self):
        """Elimina el estudiante seleccionado"""
        student = self._get_selected_student()
        if student:
            response = messagebox.askyesno("Confirmar Eliminación",
                                           f"¿Estás seguro de que quieres eliminar al estudiante:\n\n"
                                           f"ID: {student.get('student_id')}\n"
                                           f"Nombre: {student.get('student_fullname')}\n\n"
                                           "Esta acción no se puede deshacer.")

            if response:
                try:
                    success = self.controller.db_manager.delete_student(student.get('student_id'))
                    if success:
                        messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
                        self._load_students()  # Recargar datos
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el estudiante.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar estudiante: {str(e)}")
