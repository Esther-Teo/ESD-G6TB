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

# for user's inbox
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

# for tutor's inbox
class ReturnedOffer(db.Model):
    __tablename__ = 'returnedOffer'

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
            return jsonify({"code": 400,"data": {"tutorID": tutorID},"message": "Tutor already exists."}), 400
        
        createdOffer = CreatedOffer(assignmentId, data['userID'], tutorID, data['status'], data['selectedTime'], data['expectedPrice'], data['preferredDay'], False)
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(createdOffer)
        # db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify({"code": 500,"data": {"tutorID": tutorID},
        "message": "An error occurred creating the tutor account. " + str(e)}), 500

    return jsonify({"code": 201,"data": createdOffer.json()}), 201
            # "subject": subject.json()
        

# receives and stores rejected offers via POST
@app.route("/returnOffer", methods=['POST'])
def receiveReturnedOffer():
    # Check if the order contains valid JSON
    try:
        data = request.get_json()
        tutorID = data['offer']['tutorID']
        assignmentId = data['offer']['assignmentId']
        if (ReturnedOffer.query.filter_by(tutorID=tutorID, assignmentId=assignmentId).first()):
            return jsonify(
                {"code": 400,"data": {"tutorID": tutorID},"message": "Tutor already exists."}), 400
        
        returnedOffer = ReturnedOffer(assignmentId, data['offer']['userID'], tutorID, data['offer']['status'], 
                        data['offer']['selectedTime'], data['offer']['expectedPrice'], data['offer']['preferredDay'], False)
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(returnedOffer)
        # db.session.add(subject)
        db.session.commit()
    except Exception as e:
        return jsonify({"code": 500,"data": {"tutorID": tutorID},
        "message": "An error occurred creating the tutor account. " + str(e)}), 500

    return jsonify({"code": 201,"data": returnedOffer.json()}), 201
            # "subject": subject.json()


# need to create one to get all created offers by userID, update read to true, and return them in a json of jsons or smtg. 
@app.route("/created/<int:userID>", methods=['PUT', 'GET'])
def push_created(userID):
    try:
        offer = CreatedOffer.query.filter_by(userID=userID, read="!=").all()
        if offer:
            for each in offer:
                print("input")
                each.read = 1
                db.session.commit()
            return jsonify({"code": 200,"offers": [o.json() for o in offer]}), 200
            
        return jsonify({"code": 404, "data": {"userID": userID},"message": "Offer not found."}), 404

    except Exception as e:
        return jsonify({"code": 500,"data": {"userID": userID},
        "message": "An error occurred while updating the Offer. " + str(e)}), 500


@app.route("/updateStatus/<int:assignmentId>/<int:tutorID>", methods=['PUT'])
def update_status(assignmentId, tutorID):
    try:
        offer = CreatedOffer.query.filter_by(tutorID=tutorID, assignmentId=assignmentId).first()
        if not offer:
            return jsonify({"code": 404,"data": {"assignmentId": assignmentId,"tutorID": tutorID},
            "message": "Offer not found."}), 404

        offer.status = "accepted"
        offer.read = False
        db.session.commit()
        return jsonify({"code": 201, "data": {"assignmentId": assignmentId, "tutorID": tutorID}})

    except Exception as e:
        return jsonify({"code": 500,"data": {"assignmentId": assignmentId, "tutorID": tutorID},
        "message": "An error occurred while updating the Offer. " + str(e)}), 500


# need to create one to get all accepted/rejected offers by tutorID, update read to true, and return them in a json of jsons or smtg. 
@app.route("/returned/<int:tutorID>", methods=['PUT', 'GET'])
def push_returned(tutorID):
    try:
        offer = ReturnedOffer.query.filter_by(tutorID=tutorID, read="!=").all()
        if offer:
            # print("in")
            for each in offer:
                each.read = 1
                print(each.read)
                db.session.commit()
            return jsonify({"code": 200,"offers": [o.json() for o in offer]}), 200
        return jsonify({"code": 404,"data": {"tutorID": tutorID},"message": "Offer not found."}), 404

    except Exception as e:
        return jsonify({"code": 500,"data": {"tutorID": tutorID},
        "message": "An error occurred while updating the Offer. " + str(e)}), 500

# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5002, debug=True)

