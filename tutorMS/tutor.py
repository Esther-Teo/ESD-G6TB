from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from os import environ
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/tutor'# environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
CORS(app)

class Tutor(db.Model):
    __tablename__ = 'tutor'
    tutorId = db.Column(db.Integer, primary_key=True)
    tutorName = db.Column(db.String(100), nullable=False)
    tutorEmail = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(100), nullable=False)
    tutorPhone = db.Column(db.INTEGER, nullable=False)
    loc = db.Column(db.Text(1000), nullable=False)
    portfolio = db.Column(db.Text(1000))
    priceRange = db.Column(db.INTEGER, nullable=False)

    def __init__(self, tutorId, tutorName, tutorEmail, passw, tutorPhone, loc, priceRange):
        self.tutorId = tutorId
        self.tutorName = tutorName
        self.tutorEmail = tutorEmail
        self.passw = passw
        self.tutorPhone = tutorPhone
        self.loc = loc
        self.portfolio = "Tutor has not fixed their bi-ooooo :("
        self.priceRange = priceRange

    def json(self):
        return { 
            "tutorId": self.tutorId,
            "tutorName": self.tutorName, 
            "tutorEmail": self.tutorEmail, 
            "passw": self.passw, 
            "tutorPhone": self.tutorPhone, 
            "loc": self.loc,
            "priceRange": self.priceRange
            }

class TutorSubjects(db.Model):
    __tablename__ = 'tutorSubjects'
    tutorId = db.Column(db.Integer, db.ForeignKey('tutor.tutorId', ondelete="CASCADE"), primary_key=True)
    subjectId = db.Column(db.Integer, nullable=False, primary_key=True)
    pri = db.Column(db.Boolean, nullable=False)
    lvl = db.Column(db.Integer, nullable=False)
    subjects = db.Column(db.String(100), nullable=False)
    user = relationship('Tutor', backref='tutorSubjects')

    def __init__(self, tutorId, subjectId, pri, lvl, subjects):
        self.tutorId = tutorId
        self.subjectId = subjectId
        self.pri = pri
        self.lvl = lvl
        self.subjects = subjects

    def json(self):
        return { 
            "tutorId": self.tutorId, 
            "subjectId": self.subjectId, 
            "pri": self.pri, 
            "lvl": self.lvl, 
            "subjects": self.subjects
        }

# gets all tutors


@app.route("/tutor")
def get_all():
	return jsonify({"tutors": [tutor.json() for tutor in Tutor.query.all()]})

# gets one tutor + his subjects by his id



@app.route("/tutorById/<int:tutorId>")
def find_by_tutorId(tutorId):
    try:
        tutorList = Tutor.query.filter_by(tutorId = tutorId).first()
        print(tutorList)
        subject = TutorSubjects.query.filter_by(tutorId = tutorId).all()
        print(subject)
        
        if tutorList:
            return jsonify(
                {
                    "code": 200,
                    "tutorData": tutorList.json(),
                    "tutorSubject": [subj.json() for subj in subject]
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "tutorID": tutorId
                },
                "message": "Couldn't find tutor." + str(e)
            }
        ), 404

# creates a tutor
@app.route("/tutor/<int:tutorId>", methods=['POST'])
@app.route("/createTutor", methods=['POST'])
def add_tutor():
    try:
        data = request.get_json()
        tutorId = data.tutorId
        if (Tutor.query.filter_by(tutorId=tutorId).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "tutorId": tutorId
                    },
                    "message": "Tutor already exists."
                }
            ), 400
        
        tutor = Tutor(tutorId, data['tutorName'], data['tutorEmail'], data['passw'], data['tutorPhone'], data['loc'], data['portfolio'], data['priceRange'])
        subject = TutorSubjects(tutorId, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(tutor)
        db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorId": tutorId
                },
                "message": "An error occurred creating the tutor account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tutor.json(),
            "subject": subject.json()
        }
    ), 201

# edits a tutor with the given tutorid
@app.route("/updateTutor/<int:tutorId>",methods=['PUT'])
def update_tutor_details(tutorId):
    try:
        tutor = Tutor.query.filter_by(tutorId=tutorId).first()
        if not tutor:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "tutorId": tutorId
                    },
                    "message": "Tutor not found."
                }
            ), 404

        # update info
        data = request.get_json()
        if data['tutorName']:
            tutor.tutorName = data['tutorName']
        if data['passw']:
            tutor.passw = data['passw']
        if data['tutorPhone']:
            tutor.tutorPhone = data['tutorPhone']
        if data['loc']:
            tutor.loc = data['loc']
        if data['portfolio']:
            tutor.portfolio = data['portfolio']
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
                    "tutorId": tutorId
                },
                "message": "An error occurred while updating the tutor details. " + str(e)
            }
        ), 500


# gets the list of subjects by tutor
@app.route("/subjectByTutor/<int:tutorId>")
def get_tutorSubject(tutorId):
    subjectList = TutorSubjects.query.filter_by(tutorId=tutorId)
    if subjectList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tutors": [subject.json() for subject in subjectList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no subjects under this tutor."
        }
    ), 404

# creates a subject from the tutor
@app.route("/addSubject/<string:tutorId>", methods=['POST'])
def add_tutorSubject(tutorId):

    data = request.get_json()
    subjectId = data['subjectId']
    if (TutorSubjects.query.filter_by(tutorId=tutorId, subjectId=subjectId).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "tutorId": tutorId
                },
                "message": "Subject already exists."
            }
        ), 400
    subject = TutorSubjects(tutorId, subjectId, data['pri'], data['lvl'], data['subjects'])
    try:
        db.session.add(subject)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorId": tutorId
                },
                "message": "An error occurred creating the tutor subject."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": subject.json()
        }
    ), 201

# deletes a subject by the tutorid and subject id
@app.route("/deleteSubject/<int:tutorId>/<int:subjectId>", methods=['DELETE'])
def delete_subject(tutorId, subjectId):
    try:
        subject = TutorSubjects.query.filter_by(tutorId=tutorId, subjectId=subjectId).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "subjectId": subjectId
                    }
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "subjectId": subjectId
                },
                "message": "There was an error deleting the subject." + str(e)
            }
        ), 404

# edits a subject by tutorid and fetched data
@app.route("/updateSubject/<int:tutorId>/<int:subjectId>",methods=['PUT'])
def update_subject_details(tutorId, subjectId):
    try:

        subject = TutorSubjects.query.filter_by(tutorId=tutorId, subjectId=subjectId).first()
        
        data = request.get_json()

        # update info
        if data['pri']:
            subject.pri = data['pri']
        if data['lvl']:
            subject.lvl = data['lvl']
        if data['subjects']:
            subject.subjects = data['subjects']
        try:
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": subject.json()
                }
            ), 200
        
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "tutorId": tutorId
                    },
                    "message": "An error occurred while updating the tutor details. " + str(e)
                }
            ), 500

    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "tutorId": tutorId
                },
                "message": "Couldn't find tutor." + str(e)
            }
        ), 404



if __name__ == "__main__":
    app.run(port=5000, debug=True)