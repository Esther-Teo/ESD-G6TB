from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/tutor'# environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Tutor(db.Model):
    __tablename__ = 'tutor'
    tutorID = db.Column(db.String(120), primary_key=True)
    tutorName = db.Column(db.String(64), nullable=False)
    tutorPhone = db.Column(db.INTEGER, nullable=False)
    location = db.Column(db.Text(1000), nullable=False)
    portfolio = db.Column(db.Text(1000))
    teachesPri = db.Column(db.BOOLEAN, default=False)
    teachesSec = db.Column(db.BOOLEAN, default=False)
    subjects = db.Column(db.Text(1000))
    priceRange = db.Column(db.INTEGER)

    def __init__(self, tutorID, tutorName, tutorPhone, location,portfolio,teachesPri,teachesSec,subjects,priceRange):
        self.tutorID = tutorID
        self.tutorName = tutorName
        self.tutorPhone = tutorPhone
        self.location = location
        self.portfolio = portfolio
        self.teachesPri = teachesPri
        self.teachesSec = teachesSec
        self.subjects = subjects
        self.priceRange = priceRange

    def json(self):
        return {"tutorID": self.tutorID, "tutorName": self.tutorName, "tutorPhone": self.tutorPhone, "location": self.location,"portfolio": self.portfolio,"teachesPri": self.teachesPri,"teachesSec": self.teachesSec,"subjects": self.subjects,"priceRange": self.priceRange }

@app.route("/tutor")
def get_all():
    tutorList = Tutor.query.all()
    if len(tutorList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tutors": [tutor.json() for tutor in tutorList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no tutors."
        }
    ), 404
@app.route("/tutor/<string:tutorID>")
def find_by_tutorID(tutorID):
    tutor = Tutor.query.filter_by(tutorID=tutorID).first()
    if tutor:
        return jsonify(
            {
                "code": 200,
                "data": tutor.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Tutor not in database"
        }
    ), 404

@app.route("/tutor/<string:tutorID>", methods=['POST'])
def add_tutor(tutorID):
    if (Tutor.query.filter_by(tutorID=tutorID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "tutorID": tutorID
                },
                "message": "Tutor already has an account."
            }
        ), 400

    data = request.get_json()
    tutor = Tutor(tutorID, **data)

    try:
        db.session.add(tutor)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorID": tutorID
                },
                "message": "An error occurred creating the tutor account."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tutor.json()
        }
    ), 201



@app.route("/tutor/<string:tutorID>",methods=['PUT'])
def update_tutor_details(tutorID):
    try:
        tutor = Tutor.query.filter_by(tutorID=tutorID).first()
        if not tutor:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "tutorID": tutorID
                    },
                    "message": "Tutor not found."
                }
            ), 404

        # update info
        data = request.get_json()
        if data['tutorPhone']:
            tutor.tutorPhone = data['tutorPhone']
        if data['location']:
            tutor.location = data['location']
        if data['portfolio']:
            tutor.portfolio = data['portfolio']
        if data['teachesPri']:
            tutor.teachesPri = data['teachesPri']
        if data['teachesSec']:
            tutor.teachesSec = data['teachesSec']
        if data['subjects']:
            tutor.subjects = data['subjects']
        if data['priceRange']:
            tutor.priceRange = data['priceRange']
            db.session.commit()
        
            return jsonify(
                {
                    "code": 200,
                    "data": tutor.json()
                }
            ), 200
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorID": tutorID
                },
                "message": "An error occurred while updating the tutor details. " + str(e)
            }
        ), 500
if __name__ == "__main__":
    app.run(port=5000, debug=True)