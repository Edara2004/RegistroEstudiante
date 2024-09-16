from models.function_time.time_function import time_register


class GradeStudent:
    def __init__(self, id_grade_student: int, mathematics: int, physics: int, english: int, chemistry: int,
                 semester: int):
        self.id_grade_student = id_grade_student
        self.mathematics = mathematics
        self.physics = physics
        self.english = english
        self.chemistry = chemistry
        self.semester = semester
        self.time_Grade = time_register()

    def print_note(self):
        return f'name , {self.id_grade_student} {self.english}, {self.physics}, {self.mathematics}, {self.time_Grade}'


# h2 = GradeStudent(31001145, 3, 4, 4, 3, 5)  # Tests
# print(h2.print_note())
