class Student:
    def __init__(self, student_id: int, student_fullname: str, student_birthday: str, student_address: str, student_blood_type: str,
                 student_phone_number: str, student_date_of_entry: str, student_gender: str, student_email: str, student_nationality: str) -> object:
        self.student_id = student_id
        self.student_fullname = student_fullname
        self.student_birthday = student_birthday
        self.student_address = student_address
        self.student_blood_type = student_blood_type
        self.student_phone_number = student_phone_number
        self.student_date_of_entry = student_date_of_entry
        self.student_gender = student_gender
        self.student_email = student_email
        self.student_nationality = student_nationality

    def student_id(self):
        return self.student_id

    def student_fullname(self):
        return self.student_fullname

    def student_birthday(self):
        return self.student_birthday

    def student_address(self):
        return self.student_address

    def student_blood_type(self):
        return self.student_blood_type

    def student_phone_number(self):
        return self.student_phone_number

    def student_date_of_entry(self):
        return self.student_date_of_entry

    def student_gender(self):
        return self.student_gender

    def student_email(self):
        return self.student_email

    def student_nationality(self):
        return self.student_nationality


class Parents:
    def __init__(self, parents_id: int, parents_fullname: str, parents_birthday: str, parents_blood_type: str,
                 parents_phone_number: str, parents_job: str, parents_address: str,
                 parents_marital_status: str, parents_nationality: str) -> object:
        self.parents_id = parents_id
        self.parents_fullname = parents_fullname
        self.parents_birthday = parents_birthday
        self.parents_blood_type = parents_blood_type
        self.parents_phone_number = parents_phone_number
        self.parents_job = parents_job
        self.parents_address = parents_address
        self.parents_marital_status = parents_marital_status
        self.parents_nationality = parents_nationality

    def parents_id(self):
        return self.parents_id

    def parents_fullname(self):
        return self.parents_fullname

    def parents_birthday(self):
        return self.parents_birthday

    def parents_blood_type(self):
        return self.parents_blood_type

    def parents_phone_number(self):
        return self.parents_phone_number

    def parents_job(self):
        return self.parents_job

    def parents_address(self):
        return self.parents_address

    def parents_marital_status(self):
        return self.parents_marital_status

    def parents_nationality(self):
        return self.parents_nationality