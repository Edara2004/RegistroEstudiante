class StudentSubjects:
    def __init__(self, student_subjects_id: int, student_grades: str, notes=None):
        self.student_subjects_id = student_subjects_id
        self.student_grades = student_grades
        self.notes = notes or {}

    def student_subjects_id(self):
        return self.student_subjects_id

    def student_grades(self):
        return self.student_grades

    def student_notes(self):
        return self.notes

