from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Participant(db.Model):
    __tablename__ = "participant_table"

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date())
    phone_number = db.Column(db.String(15))
    address_line_1 = db.Column(db.String())
    address_line_2 = db.Column(db.String())
    post_code = db.Column(db.String())

    def __init__(self, first_name, last_name, date_of_birth, phone_number, address_line_1, address_line_2, post_code):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.post_code = post_code
        self.reference_id = self.create_unique_reference()

    def __repr__(self):
        return f"{self.reference_id}"

    def create_unique_reference(self):
        # this would call the API to create the unique id, I used epoch for now as it will be unique on single service
        return str(int(datetime.now().timestamp()))

    def as_dict(self):
        print("helloooo")
        print(self.date_of_birth)
        return {
            "reference_id": self.reference_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": datetime.strftime(self.date_of_birth, "%d/%m/%Y"),
            "phone_number": self.phone_number,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "post_code": self.post_code
        }

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_address_line_1(self, address_line_1):
        self.address_line_1 = address_line_1

    def set_address_line_2(self, address_line_2):
        self.address_line_2 = address_line_2

    def set_post_code(self, post_code):
        self.post_code = post_code

    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth


