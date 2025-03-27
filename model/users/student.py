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


class RelatedPerson:
    def __init__(self, student_id: int, related_person_id: int, relationship_type: str, related_person_fullname: str, related_person_photo: str,
                 related_person_birthday: str, related_person_blood_type: str, related_person_phone_number: str, related_person_job: str, 
                 related_person_address: str, related_person_marital_status: str, related_person_nationality: str) -> object:
        self.student_id = student_id
        self.related_person_id = related_person_id
        self.relationship_type = relationship_type
        self.related_person_fullname = related_person_fullname
        self.related_person_photo = related_person_photo
        self.related_person_birthday = related_person_birthday
        self.related_person_blood_type = related_person_blood_type
        self.related_person_phone_number = related_person_phone_number
        self.related_person_job = related_person_job
        self.related_person_address = related_person_address
        self.related_person_marital_status = related_person_marital_status
        self.related_person_nationality = related_person_nationality

    def related_person_id(self):
        return self.related_person_id

    def related_person_fullname(self):
        return self.related_person_fullname

    def related_person_birthday(self):
        return self.related_person_birthday

    def related_person_blood_type(self):
        return self.related_person_blood_type

    def related_person_phone_number(self):
        return self.related_person_phone_number

    def related_person_job(self):
        return self.related_person_job

    def related_person_address(self):
        return self.related_person_address

    def related_person_marital_status(self):
        return self.related_person_marital_status

    def related_person_nationality(self):
        return self.related_person_nationality
