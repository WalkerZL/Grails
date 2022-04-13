from datetime import datetime

from models import Participant


def test_new_participant():
    dob = datetime.strptime('01/01/1990', '%d/%m/%Y')
    participant = Participant(first_name="Jane", last_name="Doe", date_of_birth=dob, phone_number="0123456789",
                              address_line_1="123 Mayfair", address_line_2="London", post_code="LD10 ABC")
    assert participant.first_name == 'Jane'
    assert participant.last_name == 'Doe'
    assert participant.date_of_birth == dob
    assert participant.phone_number == "0123456789"
    assert participant.address_line_1 == "123 Mayfair"
    assert participant.address_line_2 == "London"
    assert participant.post_code == "LD10 ABC"
    assert participant.reference_id


def test_as_dict():
    dob = datetime.strptime('01/01/1990', '%d/%m/%Y')
    participant = Participant(first_name="Jane", last_name="Doe", date_of_birth=dob, phone_number="0123456789",
                              address_line_1="123 Mayfair", address_line_2="London", post_code="LD10 ABC")
    result = participant.as_dict()
    expected_result = {
            "reference_id": participant.reference_id,
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "01/01/1990",
            "phone_number": "0123456789",
            "address_line_1": "123 Mayfair",
            "address_line_2": "London",
            "post_code": "LD10 ABC"
        }
    assert result == expected_result
