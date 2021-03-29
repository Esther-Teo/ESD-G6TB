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
    tutorID = db.Column(db.Integer, primary_key=True)
    tutorName = db.Column(db.String(100), nullable=False)
    tutorEmail = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(100), nullable=False)
    tutorPhone = db.Column(db.INTEGER, nullable=False)
    loc = db.Column(db.Text(1000), nullable=False)
    portfolio = db.Column(db.Text(1000))
    priceRange = db.Column(db.INTEGER, nullable=False)

    def __init__(self, tutorID, tutorName, tutorEmail, passw, tutorPhone, loc, portfolio, priceRange):
        self.tutorID = tutorID
        self.tutorName = tutorName
        self.tutorEmail = tutorEmail
        self.passw = passw
        self.tutorPhone = tutorPhone
        self.loc = loc
        self.portfolio = portfolio
        self.priceRange = priceRange

    def json(self):
        return { 
            "tutorID": self.tutorID,
            "tutorName": self.tutorName, 
            "tutorEmail": self.tutorEmail, 
            "passw": self.passw, 
            "tutorPhone": self.tutorPhone, 
            "loc": self.loc, 
            "portfolio": self.portfolio, 
            "priceRange": self.priceRange
            }

class TutorSubjects(db.Model):
    __tablename__ = 'tutorSubjects'
    tutorID = db.Column(db.Integer, db.ForeignKey('tutor.tutorID', ondelete="CASCADE"), primary_key=True)
    subjectID = db.Column(db.Integer, nullable=False, primary_key=True)
    pri = db.Column(db.Boolean, nullable=False)
    lvl = db.Column(db.Integer, nullable=False)
    subjects = db.Column(db.String(100), nullable=False)
    user = relationship('Tutor', backref='tutorSubjects')

    def __init__(self, tutorID, subjectID, pri, lvl, subjects):
        self.tutorID = tutorID
        self.subjectID = subjectID
        self.pri = pri
        self.lvl = lvl
        self.subjects = subjects

    def json(self):
        return { 
            "tutorID": self.tutorID, 
            "subjectID": self.subjectID, 
            "pri": self.pri, 
            "lvl": self.lvl, 
            "subjects": self.subjects
        }

# gets all tutors
@app.route("/tutor")
def get_all():
    tutorList = Tutor.query.all()
    if len(tutorList):
        for tut in tutorList:
            tutorID = tut['tutorID']
            subjects = TutorSubjects.query.filter_by(tutorID = tutorID).all()
            tut['subjects'] = subjects
            data.append(tut.json())
        return jsonify(
            {
                "code": 200,
                "data": data
            }
    return jsonify(
        {
            "code": 404,
            "message": "There are no tutors."
        }
    ), 404

# gets one tutor + his subjects by his id
@app.route("/tutorById/<int:tutorID>")
def find_by_tutorID(tutorID):
    tutor = Tutor.query.filter_by(tutorID=tutorID).first()
    if tutor:
        for tut in tutor:
            tutorID = tut['tutorID']
            subjects = TutorSubjects.query.filter_by(tutorID = tutorID).all()
            tut['subjects'] = subjects
            data.append(tut.json())
        return jsonify(
            {
                "code": 200,
                "data": data
            }
    return jsonify(
        {
            "code": 404,
            "message": "Tutor not in database"
        }
    ), 404

# creates a tutor
@app.route("/tutor", methods=['POST'])
def add_tutor():

    data = request.get_json()
    
    tutor = Tutor(data['tutorID'], data['tutorName'], data['tutorEamil'], data['passw'], data['tutorPhone'], data['loc'], data['portfolio'], data['priceRange'] )
    subject = TutorSubjects(data['tutorID'], data['subjectID'], data['pri'], data['lvl'], data['subjects'])
    try:
        db.session.add(tutor)
        db.session.add(subject)
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
            "data": tutor.json(),
            "subject": subject.json()
        }
    ), 201

# edits a tutor with the given tutorid
@app.route("/editTutor/<int:tutorID>",methods=['PUT'])
def edit_tutor_details(tutorID):
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
                    "tutorID": tutorID
                },
                "message": "An error occurred while updating the tutor details. " + str(e)
            }
        ), 500

# gets the list of subjects by tutor
@app.route("/subjectByTutor/<int:tutorID>")
def get_tutorSubject(tutorID):
    subjectList = TutorSubjects.query.filter_by(tutorID=tutorID)
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
@app.route("/createSubject", methods=['POST'])
def add_tutorSubject():

    data = request.get_json()
    subject = TutorSubjects(**data)

    try:
        db.session.add(subject)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "msg": "oof, you fked up"
                },
                "message": "An error occurred creating the tutor account."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": subject.json()
        }
    ), 201

# deletes a subject by the tutorid and subject id
@app.route("/subject/<int:tutorID>/<int:subjectID>", methods=['DELETE'])
def delete_subject(tutorID, subjectID):
    try:
        subject = TutorSubjects.query.filter_by(tutorID=tutorID, subjectID=subjectID).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "subjectID": subjectID
                    }
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "subjectID": subjectID
                },
                "message": "There was an error deleting the subject." + str(e)
            }
        ), 404

# edits a subject by tutorid and fetched data
@app.route("/editSubject/<int:tutorID>",methods=['PUT'])
def edit_subject_details(tutorID):
    try:
        data = request.get_json()
        subID = data['subjectID']

        subject = TutorSubjects.query.filter_by(tutorID=tutorID, subjectID=subID).first()
        if not subject:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "subjectID": subjectID
                    },
                    "message": "Tutor not found."
                }
            ), 404

        # update info
        if data['pri']:
            subject.pri = data['pri']
        if data['lvl']:
            subject.lvl = data['lvl']
        if data['subjects']:
            subject.subjects = data['subjects']
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
                    "tutorID": tutorID
                },
                "message": "An error occurred while updating the tutor details. " + str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)