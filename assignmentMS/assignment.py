from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from os import environ
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/assignment'#environ.get('dbURL') #'mysql+mysqlconnector://is213@localhost:7777/book' #environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)

class Assignment(db.Model):
    __tablename__ = 'assignment'
    assignmentId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(64), nullable=False)
    childName = db.Column(db.Integer, nullable=False)
    primary = db.Column(db.Boolean, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.String(90), nullable=False)
    tutorID = db.Column(db.Integer, default=0)
    offers = relationship('Offer', cascade="all, delete-orphan")
    def __init__(self, assignmentId, userID, childName, primary, level, subject, expectedPrice, preferredDay):
        self.assignmentId = assignmentId
        self.userID = userID
        self.childName = childName
        self.primary = primary
        self.level = level
        self.subject = subject
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.tutorID = 0
 
    def json(self):
        return {
            "assignmentId": self.assignmentId, 
            "userID": self.userID, 
            "childName": self.childName, 
            "primary": self.primary, 
            "level": self.level, 
            "subject": self.subject, 
            "expectedPrice": self.expectedPrice, 
            "preferredDay": self.preferredDay
            }

class Offer(db.Model):
    __tablename__ = 'offer'

    assignmentId = db.Column(db.Integer, db.ForeignKey('assignment.assignmentId', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    tutorID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(6), nullable=False)
    selectedTime = db.Column(db.Integer, nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.String(10), nullable=False)
    assignment = db.relationship(
    'Assignment', primaryjoin='Offer.assignmentId == Assignment.assignmentId', backref='offer')
 
    def __init__(self, assignmentId, userID, tutorID, status, selectedTime, expectedPrice, preferredDay):
        self.assignmentId = assignmentId
        self.userID = userID
        self.tutorID = tutorID
        self.status = status
        self.selectedTime = selectedTime
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
 
    def json(self):
        return {
            "assignmentId": self.assignmentId, 
            "userID": self.userID,
            "tutorID": self.tutorID, 
            "status": self.status, 
            "selectedTime": self.selectedTime, 
            "expectedPrice": self.expectedPrice, 
            "preferredDay": self.preferredDay
        }


# GET all assignments (FOR TESTING ONLY!!!!)
@app.route("/assignment")
def get_all():
    return jsonify({"assignments": [assignment.json() for assignment in Assignment.query.all()]})

# GET for viewing one assignment only
@app.route("/assignmentById/<int:assignmentId>")
def find_by_assignmentId(assignmentId):
    try:
        assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
        if assignment:
            return jsonify(assignment.json())
    except Exception as e:
        return jsonify({"message": "Assignment had a problem fetching" + str(e)}), 404

# GET for viewing assignment by their user
@app.route("/assignmentByUser/<int:userID>")
def find_by_user(userID):
    try: 
        assignment = Assignment.query.filter_by(userID=userID).all()
        if assignment:
            return jsonify({"assignments": [a.json() for a in assignment]})
    except Exception as e:
        return jsonify({"message": "Assignment not found." + str(e)}), 404

# CREATE an assignment
@app.route("/makeAssignment", methods=['POST'])
def create_assignment():
    data = request.get_json()
    print(data['assignmentId'])
    assignmentId = data['assignmentId']
    if (Assignment.query.filter_by(assignmentId=assignmentId).first()):
        return jsonify({"message": "An assignment with the ID '{}' already exists.".format(assignmentId)}), 400
 
    
    assignment = Assignment(**data)
 
    try:
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "An error occurred creating the assignment." + str(e)}), 500
 
    return jsonify(assignment.json()), 201

# PUT to edit, but no use for it atm
@app.route("/assignment/<int:assignmentId>", methods=['PUT'])
def update_assignment(assignmentId):
    try:
        assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
        if assignment:
            data = request.get_json()
            if data['subject']:
                assignment.subject = data['subject']
            if data['expectedPrice']:
                assignment.expectedPrice = data['expectedPrice'] 
            if data['preferredDay']:
                assignment.preferredDay = data['preferredDay'] 
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": assignment.json()
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "data": {
                    "assignmentId": assignmentId
                },
                "message": "Assignment not found."
            }
        ), 404

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "assignmentId": assignmentId
                },
                "message": "An error occurred while updating the assignment. " + str(e)
            }
        ), 500

# DELETE an assignment by its ID
@app.route("/deleteAssignment/<int:assignmentId>", methods=['DELETE'])
def delete_assignment(assignmentId):
    try:
        assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
        if assignment:
            db.session.delete(assignment)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "assignmentId": assignmentId
                    }
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "assignmentId": assignmentId
                },
                "message": "Assignment not found." + str(e)
            }
        ), 404

# add new user using POST 
@app.route("/createOffer", methods=['POST'])
def add_offer():
    data = request.get_json()
    print(data)
    assignmentId = data['assignmentId']
    tutorID = data['tutorID']
    if (Offer.query.filter_by(assignmentId=assignmentId, tutorID=tutorID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "tutorID": tutorID
                },
                "message": "Tutor has already created an offer for this assignment."
            }
        ), 400
    offer = Offer(**data)
    try:
        
        db.session.add(offer)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID
                },
                "message": "An error occurred creating the User." + str(e)
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "data": offer.json()
        }
    ), 201

# GET offer by tutorID (tested okay)
@app.route("/offerByTutor/<int:tutorID>")
def findO_by_tutor(tutorID):
    try: 
        offer = Offer.query.filter_by(tutorID=tutorID).all()
        if offer:
            return jsonify({"offers": [a.json() for a in offer]})
    except Exception as e:
        return jsonify({"message": "Offer not found." + str(e)}), 404

# GET offer by tutorID (tested okay)
@app.route("/offerByUser/<int:userID>")
def findO_by_user(userID):
    try: 
        offer = Offer.query.filter_by(userID=userID).all()
        if offer:
            return jsonify({"offers": [a.json() for a in offer]})
    except Exception as e:
        return jsonify({"message": "Offer not found." + str(e)}), 404

# GET offer by assignmentID (tested okay)
@app.route("/offerByAssignment/<int:assignmentId>")
def findO_by_assignment(assignmentId):
    try: 
        offer = Offer.query.filter_by(assignmentId=assignmentId).all()
        if offer:
            return jsonify({"offers": [a.json() for a in offer]})
    except Exception as e:
        return jsonify({"message": "Offer not found." + str(e)}), 404

# DELETE an offer by its ID
@app.route("/deleteOffer/<int:assignmentId>/<int:tutorID>", methods=['DELETE'])
def delete_offer(assignmentId, tutorID):
    try:
        offer = Offer.query.filter_by(assignmentId=assignmentId, tutorID=tutorID).first()
        if offer:
            db.session.delete(offer)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "assignmentId": assignmentId,
                        "tutorID": tutorID
                    }
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "assignmentId": assignmentId,
                    "tutorID": tutorID
                },
                "message": "Offer had a problem deleting. " + str(e)
            }
        ), 404

# PUT to edit, but no use for it atm (NOT DONE!!!!!)
@app.route("/offer/<int:assignmentId>/<int:tutorID>", methods=['PUT'])
def update_offer(assignmentId, tutorID):
    try:
        offer = Offer.query.filter_by(assignmentId=assignmentId, tutorID=tutorID).first()
        if offer:
            data = request.get_json()
            if data['status']:
                offer.status = data['status']
            if data['selectedTime']:
                offer.selectedTime = data['selectedTime']
            if data['expectedPrice']:
                offer.expectedPrice = data['expectedPrice'] 
            if data['preferredDay']:
                offer.preferredDay = data['preferredDay'] 
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "assignmentId": assignmentId,
                        "tutorID": tutorID
                    }
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "data": {
                    "assignmentId": assignmentId,
                    "tutorID": tutorID
                },
                "message": "Offer not found."
            }
        ), 404

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "assignmentId": assignmentId,
                    "tutorID": tutorID
                },
                "message": "An error occurred while updating the Offer. " + str(e)
            }
        ), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)