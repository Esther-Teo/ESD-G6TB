from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/tutor'# environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Tutor(db.Model):
    __tablename__ = 'tutor'
    TutorID = db.Column(db.String(10), primary_key=True)
    TutorName = db.Column(db.String(64), nullable=False)
    TutorPhone = db.Column(db.INTEGER, nullable=False)
    Location = db.Column(db.Text(1000), nullable=False)
    Portfolio = db.Column(db.Text(1000))
    Subjects = db.Column(db.Text(1000))
    PriceRange = db.Column(db.INTEGER)

    def __init__(self, TutorID, TutorName, TutorPhone, Location,Portfolio,Subjects,PriceRange):
        self.TutorID = TutorID
        self.TutorName = TutorName
        self.TutorPhone = TutorPhone
        self.Location = Location
        self.Portfolio = Portfolio
        self.Subjects = Subjects
        self.PriceRange = PriceRange

    def json(self):
        return {"TutorID": self.TutorID, "TutorName": self.TutorName, "TutorPhone": self.TutorPhone, "Location": self.Location,"Portfolio": self.Portfolio,"Subjects": self.Subjects,"PriceRange": self.PriceRange }

@app.route("/tutor")
def get_all():
    tutorlist = Tutor.query.all()
    if len(tutorlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tutors": [tutor.json() for tutor in tutorlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no tutors."
        }
    ), 404
@app.route("/tutor/<string:TutorID>")
def find_by_TutorID(TutorID):
    tutor = Tutor.query.filter_by(TutorID=TutorID).first()
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

@app.route("/tutor/<string:TutorID>", methods=['POST'])
def add_tutor(TutorID):
    if (Tutor.query.filter_by(TutorID=TutorID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "TutorID": TutorID
                },
                "message": "Tutor already has an account."
            }
        ), 400

    data = request.get_json()
    tutor = Tutor(TutorID, **data)

    try:
        db.session.add(tutor)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "TutorID": TutorID
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



@app.route("/tutor/<string:TutorID>",methods=['PUT'])
def update_tutor_details(TutorID):
    try:
        tutor = Tutor.query.filter_by(TutorID=TutorID).first()
        if not tutor:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "TutorID": TutorID
                    },
                    "message": "Tutor not found."
                }
            ), 404

        # update info
        data = request.get_json()
        if data['TutorPhone']:
            tutor.TutorPhone = data['TutorPhone']
            db.session.commit()
        if data['Location']:
            tutor.Location = data['Location']
            db.session.commit()
        if data['Portfolio']:
            tutor.Portfolio = data['Portfolio']
            db.session.commit()
        if data['Subjects']:
            tutor.Subjects = data['Subjects']
            db.session.commit()
        if data['PriceRange']:
            tutor.PriceRange = data['PriceRange']
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
                    "TutorID": TutorID
                },
                "message": "An error occurred while updating the tutor details. " + str(e)
            }
        ), 500
if __name__ == "__main__":
    app.run(port=5000, debug=True)