class StudentSubjects:
    def __int__(self, id: int, notes=None):
        self.id = id
        self.notes = notes or {}