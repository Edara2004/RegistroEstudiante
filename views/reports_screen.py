import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os
from config.theme import *

class ReportsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=PRIMARY_COLOR)
        
        # Configurar grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Variables
        self.controller = controller
        self.students_data = []
        self.current_report_data = []
        
        # Crear widgets
        self._create_widgets()
        
        # Cargar datos iniciales
        self._load_students()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)  # El área de reportes ocupará el espacio
        main_frame.grid_columnconfigure(0, weight=1)

        # Frame del título
        title_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title_frame.grid_columnconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(title_frame, text="📊 Generador de Reportes", 
                               font=FONT_TITLE, background=SECONDARY_COLOR, foreground=ACCENT_COLOR)
        title_label.grid(row=0, column=0, padx=20, pady=15)

        # Contador de estudiantes
        self.count_label = ttk.Label(title_frame, text="Total: 0 estudiantes", 
                                    font=("Segoe UI", 11), background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        self.count_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Frame de controles de reportes
        controls_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Frame para tipos de reportes
        report_types_frame = tk.Frame(controls_frame, bg=SECONDARY_COLOR)
        report_types_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Etiqueta de tipos de reporte
        report_label = ttk.Label(report_types_frame, text="📋 Tipo de Reporte:", font=FONT_LABEL, 
                                background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        report_label.pack(side="left", padx=(0, 10))

        # Combobox de tipos de reporte
        self.report_type_var = tk.StringVar()
        report_types = [
            "Todos los Estudiantes",
            "Estudiantes por Género",
            "Estudiantes por Nacionalidad",
            "Estudiantes por Rango de Edad",
            "Estudiantes por Tipo de Sangre",
            "Estadísticas Generales"
        ]
        self.report_combo = ttk.Combobox(report_types_frame, textvariable=self.report_type_var, 
                                        values=report_types, state="readonly", width=25)
        self.report_combo.pack(side="left", padx=(0, 10))
        self.report_combo.set("Todos los Estudiantes")

        # Botón generar reporte
        generate_btn = ttk.Button(report_types_frame, text="🔄 Generar", 
                                 style='Primary.TButton', command=self._generate_report)
        generate_btn.pack(side="left", padx=(0, 10))

        # Frame para filtros adicionales
        filters_frame = tk.Frame(controls_frame, bg=SECONDARY_COLOR)
        filters_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Filtro por género
        gender_label = ttk.Label(filters_frame, text="Género:", font=FONT_LABEL, 
                                background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        gender_label.pack(side="left", padx=(0, 5))

        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(filters_frame, textvariable=self.gender_var, 
                                   values=["Todos", "Masculino", "Femenino", "Otro"], 
                                   state="readonly", width=10)
        gender_combo.pack(side="left", padx=(0, 15))
        gender_combo.set("Todos")

        # Filtro por nacionalidad
        nationality_label = ttk.Label(filters_frame, text="Nacionalidad:", font=FONT_LABEL, 
                                     background=SECONDARY_COLOR, foreground=PRIMARY_COLOR)
        nationality_label.pack(side="left", padx=(0, 5))

        self.nationality_var = tk.StringVar()
        self.nationality_combo = ttk.Combobox(filters_frame, textvariable=self.nationality_var, 
                                             values=["Todos"], state="readonly", width=15)
        self.nationality_combo.pack(side="left", padx=(0, 15))
        self.nationality_combo.set("Todos")

        # Frame de botones de acción
        actions_frame = tk.Frame(controls_frame, bg=SECONDARY_COLOR)
        actions_frame.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        # Botón exportar CSV
        export_csv_btn = ttk.Button(actions_frame, text="📄 Exportar CSV", 
                                   style='Success.TButton', command=self._export_to_csv)
        export_csv_btn.pack(side="right", padx=(5, 0))

        # Botón limpiar
        clear_btn = ttk.Button(actions_frame, text="🧹 Limpiar", 
                              style='Cancel.TButton', command=self._clear_report)
        clear_btn.pack(side="right", padx=(5, 0))

        # Frame del área de reportes
        report_area_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        report_area_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        report_area_frame.grid_rowconfigure(0, weight=1)
        report_area_frame.grid_columnconfigure(0, weight=1)

        # Crear área de texto para reportes
        self._create_report_area(report_area_frame)

        # Frame de botones inferiores
        bottom_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR, bd=2, relief="groove")
        bottom_frame.grid(row=3, column=0, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # Botón volver
        back_btn = ttk.Button(bottom_frame, text="⬅️ Volver al Dashboard", 
                             style='Cancel.TButton',
                             command=lambda: self.controller.show_frame(self.controller.Dashboard))
        back_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        # Botón imprimir
        print_btn = ttk.Button(bottom_frame, text="🖨️ Imprimir Reporte", 
                              style='Primary.TButton', command=self._print_report)
        print_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

    def _create_report_area(self, parent):
        """Crea el área de texto para mostrar los reportes"""
        
        # Frame para el área de texto con scrollbar
        text_container = tk.Frame(parent, bg=SECONDARY_COLOR)
        text_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        # Área de texto
        self.report_text = tk.Text(text_container, wrap="word", font=("Consolas", 10), 
                                  bg="white", fg="black", state="disabled")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.report_text.yview)
        h_scrollbar = ttk.Scrollbar(text_container, orient="horizontal", command=self.report_text.xview)
        self.report_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid del área de texto y scrollbars
        self.report_text.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

    def _load_students(self):
        """Carga los estudiantes desde la base de datos"""
        try:
            self.students_data = self.controller.db_manager.get_all_students()
            self.count_label.config(text=f"Total: {len(self.students_data)} estudiantes")
            
            # Actualizar opciones de nacionalidad
            nationalities = ["Todos"] + list(set([s.get('nationality', '') for s in self.students_data if s.get('nationality')]))
            self.nationality_combo['values'] = nationalities
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")

    def _generate_report(self):
        """Genera el reporte seleccionado"""
        try:
            report_type = self.report_type_var.get()
            gender_filter = self.gender_var.get()
            nationality_filter = self.nationality_var.get()
            
            # Aplicar filtros
            filtered_data = self._apply_filters(gender_filter, nationality_filter)
            
            # Generar reporte según el tipo
            if report_type == "Todos los Estudiantes":
                self._generate_all_students_report(filtered_data)
            elif report_type == "Estudiantes por Género":
                self._generate_gender_report(filtered_data)
            elif report_type == "Estudiantes por Nacionalidad":
                self._generate_nationality_report(filtered_data)
            elif report_type == "Estudiantes por Rango de Edad":
                self._generate_age_range_report(filtered_data)
            elif report_type == "Estudiantes por Tipo de Sangre":
                self._generate_blood_type_report(filtered_data)
            elif report_type == "Estadísticas Generales":
                self._generate_general_stats_report(filtered_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")

    def _apply_filters(self, gender_filter, nationality_filter):
        """Aplica filtros a los datos"""
        filtered = self.students_data.copy()
        
        if gender_filter != "Todos":
            filtered = [s for s in filtered if s.get('gender') == gender_filter]
        
        if nationality_filter != "Todos":
            filtered = [s for s in filtered if s.get('nationality') == nationality_filter]
        
        return filtered

    def _generate_all_students_report(self, data):
        """Genera reporte de todos los estudiantes"""
        self.current_report_data = data
        
        report = f"""
{'='*80}
                    REPORTE DE TODOS LOS ESTUDIANTES
{'='*80}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de estudiantes: {len(data)}

{'ID':<8} {'Nombre':<30} {'Género':<10} {'Edad':<6} {'Nacionalidad':<15} {'Teléfono':<15}
{'-'*80}
"""
        
        for student in data:
            age = self._calculate_age(student.get('birthday', ''))
            report += f"{student.get('student_id', ''):<8} "
            report += f"{student.get('student_fullname', '')[:28]:<30} "
            report += f"{student.get('gender', '')[:8]:<10} "
            report += f"{age:<6} "
            report += f"{student.get('nationality', '')[:13]:<15} "
            report += f"{student.get('phone_number', 'N/A')[:13]:<15}\n"
        
        self._display_report(report)

    def _generate_gender_report(self, data):
        """Genera reporte por género"""
        gender_counts = {}
        for student in data:
            gender = student.get('gender', 'No especificado')
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        report = f"""
{'='*60}
                    REPORTE POR GÉNERO
{'='*60}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de estudiantes: {len(data)}

{'Género':<15} {'Cantidad':<10} {'Porcentaje':<12}
{'-'*40}
"""
        
        for gender, count in gender_counts.items():
            percentage = (count / len(data)) * 100 if data else 0
            report += f"{gender:<15} {count:<10} {percentage:.1f}%\n"
        
        self._display_report(report)

    def _generate_nationality_report(self, data):
        """Genera reporte por nacionalidad"""
        nationality_counts = {}
        for student in data:
            nationality = student.get('nationality', 'No especificada')
            nationality_counts[nationality] = nationality_counts.get(nationality, 0) + 1
        
        report = f"""
{'='*60}
                    REPORTE POR NACIONALIDAD
{'='*60}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de estudiantes: {len(data)}

{'Nacionalidad':<20} {'Cantidad':<10} {'Porcentaje':<12}
{'-'*45}
"""
        
        for nationality, count in nationality_counts.items():
            percentage = (count / len(data)) * 100 if data else 0
            report += f"{nationality:<20} {count:<10} {percentage:.1f}%\n"
        
        self._display_report(report)

    def _generate_age_range_report(self, data):
        """Genera reporte por rango de edad"""
        age_ranges = {
            '0-17': 0,
            '18-25': 0,
            '26-35': 0,
            '36-50': 0,
            '50+': 0
        }
        
        for student in data:
            age = self._calculate_age(student.get('birthday', ''))
            if age == 'N/A':
                continue
            
            try:
                age_num = int(age)
                if age_num <= 17:
                    age_ranges['0-17'] += 1
                elif age_num <= 25:
                    age_ranges['18-25'] += 1
                elif age_num <= 35:
                    age_ranges['26-35'] += 1
                elif age_num <= 50:
                    age_ranges['36-50'] += 1
                else:
                    age_ranges['50+'] += 1
            except:
                continue
        
        report = f"""
{'='*60}
                    REPORTE POR RANGO DE EDAD
{'='*60}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de estudiantes: {len(data)}

{'Rango de Edad':<15} {'Cantidad':<10} {'Porcentaje':<12}
{'-'*40}
"""
        
        for age_range, count in age_ranges.items():
            percentage = (count / len(data)) * 100 if data else 0
            report += f"{age_range:<15} {count:<10} {percentage:.1f}%\n"
        
        self._display_report(report)

    def _generate_blood_type_report(self, data):
        """Genera reporte por tipo de sangre"""
        blood_type_counts = {}
        for student in data:
            blood_type = student.get('blood_type', 'No especificado')
            blood_type_counts[blood_type] = blood_type_counts.get(blood_type, 0) + 1
        
        report = f"""
{'='*60}
                    REPORTE POR TIPO DE SANGRE
{'='*60}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de estudiantes: {len(data)}

{'Tipo de Sangre':<15} {'Cantidad':<10} {'Porcentaje':<12}
{'-'*40}
"""
        
        for blood_type, count in blood_type_counts.items():
            percentage = (count / len(data)) * 100 if data else 0
            report += f"{blood_type:<15} {count:<10} {percentage:.1f}%\n"
        
        self._display_report(report)

    def _generate_general_stats_report(self, data):
        """Genera reporte de estadísticas generales"""
        if not data:
            report = "No hay datos para generar estadísticas."
            self._display_report(report)
            return
        
        # Calcular estadísticas
        total_students = len(data)
        genders = [s.get('gender') for s in data if s.get('gender')]
        nationalities = [s.get('nationality') for s in data if s.get('nationality')]
        blood_types = [s.get('blood_type') for s in data if s.get('blood_type')]
        
        ages = []
        for student in data:
            age = self._calculate_age(student.get('birthday', ''))
            if age != 'N/A':
                try:
                    ages.append(int(age))
                except:
                    continue
        
        report = f"""
{'='*70}
                        ESTADÍSTICAS GENERALES
{'='*70}
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESUMEN GENERAL:
• Total de estudiantes: {total_students}
• Géneros únicos: {len(set(genders))}
• Nacionalidades únicas: {len(set(nationalities))}
• Tipos de sangre registrados: {len(set(blood_types))}

DISTRIBUCIÓN POR GÉNERO:
"""
        
        gender_counts = {}
        for gender in genders:
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        for gender, count in gender_counts.items():
            percentage = (count / total_students) * 100
            report += f"  • {gender}: {count} ({percentage:.1f}%)\n"
        
        if ages:
            avg_age = sum(ages) / len(ages)
            min_age = min(ages)
            max_age = max(ages)
            report += f"""
DISTRIBUCIÓN POR EDAD:
  • Edad promedio: {avg_age:.1f} años
  • Edad mínima: {min_age} años
  • Edad máxima: {max_age} años
"""
        
        report += f"""
NACIONALIDADES MÁS COMUNES:
"""
        nationality_counts = {}
        for nationality in nationalities:
            nationality_counts[nationality] = nationality_counts.get(nationality, 0) + 1
        
        # Top 5 nacionalidades
        top_nationalities = sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for nationality, count in top_nationalities:
            percentage = (count / total_students) * 100
            report += f"  • {nationality}: {count} ({percentage:.1f}%)\n"
        
        self._display_report(report)

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

    def _display_report(self, report_text):
        """Muestra el reporte en el área de texto"""
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report_text)
        self.report_text.config(state="disabled")

    def _export_to_csv(self):
        """Exporta el reporte actual a CSV"""
        if not self.current_report_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar. Genera un reporte primero.")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar reporte como CSV"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['ID', 'Nombre', 'Género', 'Edad', 'Teléfono', 'Email', 'Nacionalidad', 'Tipo Sangre', 'Fecha Ingreso']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for student in self.current_report_data:
                        age = self._calculate_age(student.get('birthday', ''))
                        writer.writerow({
                            'ID': student.get('student_id', ''),
                            'Nombre': student.get('student_fullname', ''),
                            'Género': student.get('gender', ''),
                            'Edad': age,
                            'Teléfono': student.get('phone_number', ''),
                            'Email': student.get('email', ''),
                            'Nacionalidad': student.get('nationality', ''),
                            'Tipo Sangre': student.get('blood_type', ''),
                            'Fecha Ingreso': student.get('date_of_entry', '')
                        })
                
                messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV: {str(e)}")

    def _clear_report(self):
        """Limpia el área de reportes"""
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.config(state="disabled")
        self.current_report_data = []

    def _print_report(self):
        """Simula la impresión del reporte"""
        if not self.current_report_data:
            messagebox.showwarning("Advertencia", "No hay reporte para imprimir. Genera un reporte primero.")
            return
        
        messagebox.showinfo("Imprimir", "Funcionalidad de impresión se implementará próximamente.\n\n"
                                       "Por ahora puedes usar la función de exportar a CSV.") 