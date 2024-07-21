
from ctr_data.function_time.time_function import time_register


class Notes:
    def __init__(self, id_student_notes: int, mathematics: int, physics: int, english: int, ):
        self.id_student_notes = id_student_notes
        self.mathematics = mathematics
        self.physics = physics
        self.english = english
        self.time_check = time_register()

    def print_note(self):
        return f'name , {self.id_student_notes} {self.english}, {self.physics}, {self.mathematics}, {self.time_check}'


h2 = Notes(31001145, 3, 4, 4) # Tests
print(h2.print_note())
