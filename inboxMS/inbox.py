import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from os import environ
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/inbox'# environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
CORS(app)

class RejectedOffer(db.Model):
    __tablename__ = 'rejectedOffer'

    assignmentId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    tutorID = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(6), nullable=False)
    selectedTime = db.Column(db.Integer, nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.String(10), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
 
    def __init__(self, assignmentId, userID, tutorID, status, selectedTime, expectedPrice, preferredDay, read):
        self.assignmentId = assignmentId
        self.userID = userID
        self.tutorID = tutorID
        self.status = status
        self.selectedTime = selectedTime
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.read = read
 
    def json(self):
        return {
            "assignmentId": self.assignmentId, 
            "userID": self.userID,
            "tutorID": self.tutorID, 
            "status": self.status,
            "selectedTime": self.selectedTime, 
            "expectedPrice": self.expectedPrice, 
            "preferredDay": self.preferredDay,
            "read": self.read
        }

class CreatedOffer(db.Model):
    __tablename__ = 'createdOffer'

    assignmentId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    tutorID = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(6), nullable=False)
    selectedTime = db.Column(db.Integer, nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.String(10), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
 
    def __init__(self, assignmentId, userID, tutorID, status, selectedTime, expectedPrice, preferredDay, read):
        self.assignmentId = assignmentId
        self.userID = userID
        self.tutorID = tutorID
        self.status = status
        self.selectedTime = selectedTime
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.read = read
 
    def json(self):
        return {
            "assignmentId": self.assignmentId, 
            "userID": self.userID,
            "tutorID": self.tutorID, 
            "status": self.status,
            "selectedTime": self.selectedTime, 
            "expectedPrice": self.expectedPrice, 
            "preferredDay": self.preferredDay,
            "read": self.read
        }
class AcceptedOffer(db.Model):
    __tablename__ = 'acceptedOffer'

    assignmentId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    tutorID = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(6), nullable=False)
    selectedTime = db.Column(db.Integer, nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.String(10), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
 
    def __init__(self, assignmentId, userID, tutorID, status, selectedTime, expectedPrice, preferredDay, read):
        self.assignmentId = assignmentId
        self.userID = userID
        self.tutorID = tutorID
        self.status = status
        self.selectedTime = selectedTime
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.read = read
 
    def json(self):
        return {
            "assignmentId": self.assignmentId, 
            "userID": self.userID,
            "tutorID": self.tutorID, 
            "status": self.status,
            "selectedTime": self.selectedTime, 
            "expectedPrice": self.expectedPrice, 
            "preferredDay": self.preferredDay,
            "read": self.read
        }

# receives and stores created offers via POST
@app.route("/createOffer", methods=['POST'])
def receiveCreatedOffer():
    # Check if the order contains valid JSON
    try:
        data = request.get_json()
        tutorID = data['tutorID']
        assignmentId = data['assignmentId']
        if (CreatedOffer.query.filter_by(tutorID=tutorID, assignmentId=assignmentId).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "tutorID": tutorID
                    },
                    "message": "Tutor already exists."
                }
            ), 400
        
        createdOffer = CreatedOffer(assignmentId, data['userID'], tutorID, data['status'], data['selectedTime'], data['expectedPrice'], data['preferredDay'], False)
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(createdOffer)
        # db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorID": tutorID
                },
                "message": "An error occurred creating the tutor account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": createdOffer.json(),
            # "subject": subject.json()
        }
    ), 201

# receives and stores rejected offers via POST
@app.route("/rejectOffer", methods=['POST'])
def receiveRejectedOffer():
    # Check if the order contains valid JSON
    try:
        data = request.get_json()
        tutorID = data['tutorID']
        assignmentId = data['assignmentId']
        if (RejectedOffer.query.filter_by(tutorID=tutorID, assignmentId=assignmentId).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "tutorID": tutorID
                    },
                    "message": "Tutor already exists."
                }
            ), 400
        
        rejectedOffer = RejectedOffer(assignmentId, data['userID'], tutorID, data['status'], data['selectedTime'], data['expectedPrice'], data['preferredDay'], False)
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(rejectedOffer)
        # db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorID": tutorID
                },
                "message": "An error occurred creating the tutor account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": rejectedOffer.json(),
            # "subject": subject.json()
        }
    ), 201

# receives and stores accepted offers via POST
@app.route("/acceptOffer", methods=['POST'])
def receiveAcceptedOffer():
    # Check if the order contains valid JSON
    try:
        data = request.get_json()
        tutorID = data['tutorID']
        assignmentId = data['assignmentId']
        if (AcceptedOffer.query.filter_by(tutorID=tutorID, assignmentId=assignmentId).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "tutorID": tutorID
                    },
                    "message": "Tutor already exists."
                }
            ), 400
        
        acceptedOffer = AcceptedOffer(assignmentId, data['userID'], tutorID, data['status'], data['selectedTime'], data['expectedPrice'], data['preferredDay'], False)
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(acceptedOffer)
        # db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "tutorID": tutorID
                },
                "message": "An error occurred creating the tutor account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": acceptedOffer.json(),
            # "subject": subject.json()
        }
    ), 201



# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5002, debug=True)

