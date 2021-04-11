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
    stripeID = db.Column(db.String(100), nullable=False)

    def __init__(self, tutorID, tutorName, tutorEmail, passw, tutorPhone, loc, portfolio, priceRange,stripeID):
        self.tutorID = tutorID
        self.tutorName = tutorName
        self.tutorEmail = tutorEmail
        self.passw = passw
        self.tutorPhone = tutorPhone
        self.loc = loc
        self.portfolio = portfolio
        self.priceRange = priceRange
        self.stripeID = stripeID

    def json(self):
        return { 
            "tutorID": self.tutorID,
            "tutorName": self.tutorName, 
            "tutorEmail": self.tutorEmail, 
            "passw": self.passw, 
            "tutorPhone": self.tutorPhone, 
            "loc": self.loc,
            "portfolio": self.portfolio,
            "priceRange": self.priceRange,
            "stripeID": self.stripeID
            }


# gets all tutors
@app.route("/tutor")
def get_all():
	return jsonify({"tutors": [tutor.json() for tutor in Tutor.query.all()]})


#retrieve stripe ID based on Tutor ID 

@app.route("/retrieve_stripe_id", methods=['POST', 'GET'])
def retrieve_stripe_id():
    data = request.get_json()
    print(data)
    tutorID = data['tutorID']

    print(f"tutorID: {tutorID}")
    try:
        # tutor = Tutor.query.filter_by(tutorID=tutorID).first()
        # Tutor.query.filter_by(tutorID=tutorID).first()
        res = Tutor.query.filter_by(tutorID=tutorID).first()
        print(res)
        if (res):
            print("runs?")
            print(res)
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message":"returns",
                        "tutorID": res.tutorID,
                        "tutorName": res.tutorName,
                        "tutorEmail": res.tutorEmail,
                        "stripeID": res.stripeID
                    },
                    "message": "Stripe Id Returned"
                }
            ), 200
    except Exception as e:
        print("why error??")    
        return jsonify(
            {
                "code": 404,
                "message": "There was an error" + str(e)
            }), 404


# creates a tutor
@app.route("/createTutor", methods=['POST'])
def add_tutor():
    try:
        data = request.get_json()
        tutorID = data['tutorID']
        if (Tutor.query.filter_by(tutorID=tutorID).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "tutorID": tutorID
                    },
                    "message": "Tutor already exists."
                }
            ), 400
        
        tutor = Tutor(tutorID, data['tutorName'], data['tutorEmail'], data['passw'], data['tutorPhone'], data['loc'], data['portfolio'], data['priceRange'],data['stripeID'])
        # subject = TutorSubjects(tutorID, data['subjectId'], data['pri'], data['lvl'], data['subjects'])
        db.session.add(tutor)
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
            "data": tutor.json(),
            # "subject": subject.json()
        }
    ), 201

# edits a tutor with the given tutorid
@app.route("/updateTutor/<int:tutorID>",methods=['PUT'])
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

# checks/authenticates the tutor
@app.route("/tutorcheck", methods=['POST', 'GET'])
def check_tutor():
    data = request.get_json()
    # print(data)
    email = data['tutorEmail']
    # email= "mikescarn@gmail.com"
    passw = data['password']
    # passw="helps"
    try:
        res = Tutor.query.filter_by(tutorEmail=email, passw=passw).first()
        if (res):
            print(res)
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message":"meep",
                        "tutorID": res.tutorID,
                        "tutorName": res.tutorName,
                        "tutorEmail": res.tutorEmail
                    },
                    "message": "Tutor authenticated."
                }
            ), 200
    except Exception as e:

        return jsonify(
            {
                "code": 404,
                "message": "There was an error" + str(e)
            }), 404


# check tutor google log in 
# port 5006 
@app.route("/tutorgoogle", methods=['POST', 'GET'])
def check_google_tutor():
    data = request.get_json()
    # print(data)
    email = data['tutorEmail']
    # email= "mikescarn@gmail.com"
    
    try:
        res = Tutor.query.filter_by(tutorEmail=email).first()
        if (res):
            # print(res)
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message":"meep",
                        "tutorID": res.tutorID,
                        "tutorName": res.tutorName,
                        "tutorEmail": res.tutorEmail
                    },
                    "message": "User authenticated."
                }
            ), 200
    except Exception as e:

        return jsonify(
            {
                "code": 404,
                "message": "There was an error" + str(e),
                "display": "none found"
            }), 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)
# class TutorSubjects(db.Model):
#     __tablename__ = 'tutorSubjects'
#     tutorID = db.Column(db.Integer, db.ForeignKey('tutor.tutorID', ondelete="CASCADE"), primary_key=True)
#     subjectId = db.Column(db.Integer, nullable=False, primary_key=True)
#     pri = db.Column(db.Boolean, nullable=False)
#     lvl = db.Column(db.Integer, nullable=False)
#     subjects = db.Column(db.String(100), nullable=False)
#     user = relationship('Tutor', backref='tutorSubjects')

#     def __init__(self, tutorID, subjectId, pri, lvl, subjects):
#         self.tutorID = tutorID
#         self.subjectId = subjectId
#         self.pri = pri
#         self.lvl = lvl
#         self.subjects = subjects

#     def json(self):
#         return { 
#             "tutorID": self.tutorID, 
#             "subjectId": self.subjectId, 
#             "pri": self.pri, 
#             "lvl": self.lvl, 
#             "subjects": self.subjects
#         }


# # gets the list of subjects by tutor
# @app.route("/subjectByTutor/<int:tutorID>")
# def get_tutorSubject(tutorID):
#     subjectList = TutorSubjects.query.filter_by(tutorID=tutorID)
#     if subjectList:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "tutors": [subject.json() for subject in subjectList]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no subjects under this tutor."
#         }
#     ), 404

# # creates a subject from the tutor
# @app.route("/addSubject/<string:tutorID>", methods=['POST'])
# def add_tutorSubject(tutorID):

#     data = request.get_json()
#     subjectId = data['subjectId']
#     if (TutorSubjects.query.filter_by(tutorID=tutorID, subjectId=subjectId).first()):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "tutorID": tutorID
#                 },
#                 "message": "Subject already exists."
#             }
#         ), 400
#     subject = TutorSubjects(tutorID, subjectId, data['pri'], data['lvl'], data['subjects'])
#     try:
#         db.session.add(subject)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "tutorID": tutorID
#                 },
#                 "message": "An error occurred creating the tutor subject."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": subject.json()
#         }
#     ), 201

# # deletes a subject by the tutorid and subject id
# @app.route("/deleteSubject/<int:tutorID>/<int:subjectId>", methods=['DELETE'])
# def delete_subject(tutorID, subjectId):
#     try:
#         subject = TutorSubjects.query.filter_by(tutorID=tutorID, subjectId=subjectId).first()
#         if subject:
#             db.session.delete(subject)
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": {
#                         "subjectId": subjectId
#                     }
#                 }
#             )
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 404,
#                 "data": {
#                     "subjectId": subjectId
#                 },
#                 "message": "There was an error deleting the subject." + str(e)
#             }
#         ), 404

# # edits a subject by tutorid and fetched data
# @app.route("/updateSubject/<int:tutorID>/<int:subjectId>",methods=['PUT'])
# def update_subject_details(tutorID, subjectId):
#     try:

#         subject = TutorSubjects.query.filter_by(tutorID=tutorID, subjectId=subjectId).first()
        
#         data = request.get_json()

#         # update info
#         if data['pri']:
#             subject.pri = data['pri']
#         if data['lvl']:
#             subject.lvl = data['lvl']
#         if data['subjects']:
#             subject.subjects = data['subjects']
#         try:
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": subject.json()
#                 }
#             ), 200
        
#         except Exception as e:
#             return jsonify(
#                 {
#                     "code": 500,
#                     "data": {
#                         "tutorID": tutorID
#                     },
#                     "message": "An error occurred while updating the tutor details. " + str(e)
#                 }
#             ), 500

#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 404,
#                 "data": {
#                     "tutorID": tutorID
#                 },
#                 "message": "Couldn't find tutor." + str(e)
#             }
#         ), 404


# # gets one tutor + his subjects by his id
# @app.route("/tutor/<int:tutorID>",methods=['GET'])
# def find_by_tutorId(tutorID):
#     try:
#         tutorList = Tutor.query.filter_by(tutorID = tutorID).first()
#         print(tutorList)
#         subject = TutorSubjects.query.filter_by(tutorID = tutorID).all()
#         print(subject)
        
#         if tutorList:
#             return jsonify(
#                 {
#                     "code": 200,
#                     "tutorData": tutorList.json(),
#                     "tutorSubject": [subj.json() for subj in subject]
#                 }
#             )
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 404,
#                 "data": {
#                     "tutorID": tutorID
#                 },
#                 "message": "Couldn't find tutor." + str(e)
#             }
#         ), 404
