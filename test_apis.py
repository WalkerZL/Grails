import json

import pytest

from main import create_app
from models import db

new_participant = {
    "first_name": "Joe",
    "last_name": "Bloggs",
    "date_of_birth": "01/08/2011",
    "phone_number": "01947 847345",
    "address_line_1": "14 A Street",
    "address_line_2": "Derbyshire",
    "post_code": "DB1 2RU"
}


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"
    })
    testing_client = flask_app.test_client()
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield db
    db.drop_all()


def test_get_empty_participants_list(test_client):
    response = test_client.get('/participants')
    assert response.status_code == 200
    assert [] == json.loads(response.data)


def test_add_and_delete_participant(test_client):
    # check empty
    response = test_client.get("/participants")
    assert [] == json.loads(response.data)

    response = test_client.post("/participants/new", data=json.dumps(new_participant))
    assert "Participant created successfully" == response.data.decode()
    assert 200 == response.status_code

    # check record added
    response = test_client.get("/participants")
    response_json = json.loads(response.data)
    assert response_json[0]["first_name"] == "Joe"
    assert response_json[0]["last_name"] == "Bloggs"
    assert response_json[0]["address_line_1"] == "14 A Street"
    assert response_json[0]["address_line_2"] == "Derbyshire"
    assert response_json[0]["post_code"] == "DB1 2RU"
    assert response_json[0]["phone_number"] == "01947 847345"
    assert response_json[0]["date_of_birth"] == "01/08/2011"
    assert response_json[0]["reference_id"]

    # delete record
    reference_id = response_json[0]["reference_id"]
    response = test_client.delete(f"/participants/{reference_id}/delete")
    assert "Participant deleted successfully" == response.data.decode()
    assert 200 == response.status_code

    # check empty
    response = test_client.get("/participants")
    assert [] == json.loads(response.data)


def test_update_participant(test_client):
    # add participant
    response = test_client.post("/participants/new", data=json.dumps(new_participant))
    assert "Participant created successfully" == response.data.decode()
    assert 200 == response.status_code

    # get reference id
    response = test_client.get("/participants")
    response_json = json.loads(response.data)
    reference_id = response_json[0]["reference_id"]

    # update participant
    updated_values = {
        "first_name": "Jane",
        "date_of_birth": "02/08/2011",
        "phone_number": "01947 847355",
        "address_line_1": "15 A Street"
    }
    response = test_client.patch(f"/participants/{reference_id}/update", data=json.dumps(updated_values))
    assert "Participant updated successfully" == response.data.decode()
    assert 200 == response.status_code

    # check new values
    response = test_client.get(f"/participants/{reference_id}")
    response_json = json.loads(response.data)
    assert response_json['first_name'] == "Jane"
    assert response_json['last_name'] == "Bloggs"
    assert response_json['address_line_1'] == "15 A Street"
    assert response_json['address_line_2'] == "Derbyshire"
    assert response_json['post_code'] == "DB1 2RU"
    assert response_json['phone_number'] == "01947 847355"
    assert response_json['date_of_birth'] == "02/08/2011"
    assert response_json['reference_id'] == reference_id

    # delete record
    response = test_client.delete(f"/participants/{reference_id}/delete")
    assert "Participant deleted successfully" == response.data.decode()
    assert 200 == response.status_code


def test_add_person_with_invalid_date(test_client):
    with pytest.raises(ValueError):
        incorrect_dob_participant = new_participant
        incorrect_dob_participant["date_of_birth"] = "2011-08-01"
        response = test_client.post("/participants/new", data=json.dumps(incorrect_dob_participant))
        assert "Invalid date format, format required: DD/MM/YYYY" == response.data.decode()
        assert 400 == response.status_code


def test_get_participant_with_unknown_reference_id(test_client):
    response = test_client.get("/participants/REFERENCE")
    assert "Participant with reference id REFERENCE doesn't exist" == response.data.decode()
    assert 404 == response.status_code


def test_update_participant_with_unknown_reference_id(test_client):
    updated_values = {
        "phone_number": "01234565432"
    }
    response = test_client.patch("/participants/REFERENCE/update", data=json.dumps(updated_values))
    assert "Participant with reference id REFERENCE doesn't exist" == response.data.decode()
    assert 404 == response.status_code


def test_delete_participant_with_unknown_reference_id(test_client):
    response = test_client.delete("/participants/REFERENCE/delete")
    assert "Participant with reference id REFERENCE doesn't exist" == response.data.decode()
    assert 404 == response.status_code
