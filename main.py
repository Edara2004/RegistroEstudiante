class Student:
    def __init__(self, id_student: int, name: str, birthday: str, nationality: str, gender: str, email: str,
                 register: str, semester: int, career: str):
        self.id_student = id_student
        self.name = name
        self.birthday = birthday
        self.nationality = nationality
        self.gender = gender
        self.email = email
        self.register = register
        self.semester = semester
        self.career = career

    def student_data(self):
        return f'Data, {self.id_student}, {self.name}, {self.birthday}, {self.nationality}, {self.gender}, {self.email}, {self.register}, {self.semester}, {self.career}'

    def id_student(self):
        return self.id_student

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
