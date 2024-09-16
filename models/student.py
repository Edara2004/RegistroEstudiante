
class Student:
    def __init__(self, id_student_m: int, name: str, birthday: str, nationality: str, gender: str, email: str,
                 register: str, semester: int, career: str) -> object:
        self.id_student = id_student_m
        self.name = name
        self.birthday = birthday
        self.nationality = nationality
        self.gender = gender
        self.email = email
        self.register = register
        self.semester = semester
        self.career = career

    def show_student_data(self):
        return f'Data, {self.id_student_m}, {self.name}, {self.birthday}, {self.nationality}, {self.gender}, {self.email}, {self.register}, {self.semester}, {self.career}'

    def id_student_m(self):
        return self.id_student_m

    def name(self):
        return self.name

    def birthday(self):
        return self.birthday

    def nationality(self):
        return self.nationality

    def gender(self):
        return self.gender

    def email(self):
        return self.email

    def register(self):
        return self.register

    def semester(self):
        return self.semester

    def career(self):
        return self.career


# h2 = Notes(2, 3, 4)
# print(h2.print_note())


# a = Student(3204565, "Marco Ayala", "2002-05-10", "Venezuela", "Masculino", "peppa_pig_magica@gmail.com", "Si", 5,"Sistemas")
# print(a.show_student_data())
