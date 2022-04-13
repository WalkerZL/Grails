import json
from datetime import datetime

from flask import Flask, request, jsonify, Response
from models import db, Participant


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///participants.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    @app.route("/participants/new", methods=["POST"])
    def new():
        request_params = json.loads(request.data)
        first_name = request_params["first_name"]
        last_name = request_params["last_name"]
        date_of_birth = datetime.strptime(request_params["date_of_birth"], "%d/%m/%Y")
        phone_number = request_params["phone_number"]
        address_line_1 = request_params["address_line_1"]
        address_line_2 = request_params["address_line_2"]
        post_code = request_params["post_code"]
        participant = Participant(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, phone_number=phone_number,
                                  address_line_1=address_line_1, address_line_2=address_line_2, post_code=post_code)
        db.session.add(participant)
        db.session.commit()
        return "Participant created successfully"

    @app.route("/participants", methods=["GET"])
    def retrieve_participants_list():
        participants = Participant.query.all()
        json_data = []
        for participant in participants:
            json_data.append(participant.as_dict())
        return jsonify(json_data)

    @app.route("/participants/<string:reference_id>", methods=["GET"])
    def retrieve_participant(reference_id):
        participant = Participant.query.filter_by(reference_id=reference_id).first()
        if participant:
            return jsonify(participant.as_dict())
        return Response(f"Participant with reference id {reference_id} doesn't exist", 404)

    @app.route("/participants/<string:reference_id>/update", methods=["PATCH"])
    def update(reference_id):
        participant = Participant.query.filter_by(reference_id=reference_id).first()
        if participant:
            request_params = json.loads(request.data)
            if "date_of_birth" in request_params.keys():
                try:
                    date = datetime.strptime(request_params["date_of_birth"], "%d/%m/%Y")
                    participant.set_date_of_birth(date)
                except ValueError:
                    return Response(f"Invalid date format, format required: DD/MM/YYYY", 400)
            fields = ["phone_number", "first_name", "last_name", "address_line_1", "address_line_2", "post_code"]
            for field in fields:
                if field in request_params.keys():
                    update_participant_field(participant, field, request_params[field])
            db.session.commit()
            return "Participant updated successfully"
        return Response(f"Participant with reference id {reference_id} doesn't exist", 404)

    @app.route("/participants/<string:reference_id>/delete", methods=["DELETE"])
    def delete(reference_id):
        participant = Participant.query.filter_by(reference_id=reference_id).first()
        if participant:
            db.session.delete(participant)
            db.session.commit()
            return "Participant deleted successfully"
        return Response(f"Participant with reference id {reference_id} doesn't exist", 404)

    def update_participant_field(participant, field, value):
        function_name = f"set_{field}"
        getattr(participant, function_name)(value)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=5000)
