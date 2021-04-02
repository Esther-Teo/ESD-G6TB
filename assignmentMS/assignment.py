from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
    preferredDay = db.Column(db.Integer, nullable=False)
    tutorId = db.Column(db.Integer, default=0)
 
    def __init__(self, assignmentId, userID, childName, primary, level, subject, location, expectedPrice, preferredDay):
        self.assignmentId = assignmentId
        self.userID = userID
        self.childName = childName
        self.primary = primary
        self.level = level
        self.subject = subject
        self.location = location
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.tutorId = 0
 
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

# GET all assignments (FOR TESTING ONLY!!!!)
@app.route("/assignment")
def get_all():
    return jsonify({"assignments": [assignment.json() for assignment in Assignment.query.all()]})

# GET for viewing one assignment only
@app.route("/assignmentById/<int:assignmentId>")
def find_by_assignmentId(assignmentId):
    assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
    if assignment:
        return jsonify(assignment.json)
    return jsonify({"message": "Assignment not found."}), 404

# GET for viewing assignment by their user
@app.route("/assignmentByUser/<int:userID>")
def find_by_user(userID):
    assignment = Assignment.query.filter_by(userID=userID).all()
    if assignment:
        return jsonify({"assignments": [a.json() for a in assignment]})
    return jsonify({"message": "Assignment not found."}), 404

# Creates an assignment
@app.route("/assignment", methods=['POST'])
def create_assignment():
    data = request.get_json()
    print(data)
    assignmentId = data.assignmentId
    if (Assignment.query.filter_by(assignmentId=assignmentId).first()):
        return jsonify({"message": "An assignment with the ID '{}' already exists.".format(assignmentId)}), 400
 
    
    assignment = Assignment(**data)
 
    try:
        db.session.add(assignment)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the assignment."}), 500
 
    return jsonify(assignment.json()), 201

# to edit, but no use for it atm
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

# Deletes an assignment by its ID
@app.route("/assignment/<int:assignmentId>", methods=['DELETE'])
def delete_assignment(assignmentId):
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
    return jsonify(
        {
            "code": 404,
            "data": {
                "assignmentId": assignmentId
            },
            "message": "Assignment not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)