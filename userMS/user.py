from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import relationship
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), nullable=False)
    userEmail = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(20), nullable=False)
    userPhone = db.Column(db.Integer, nullable=False)
    loc = db.Column(db.String(1000), nullable=False)

    def __init__(self, userID, userName, userEmail, passw,  userPhone, loc):
        self.userID = userID
        self.userName = userName
        self.userEmail = userEmail
        self.passw = passw
        self.userPhone = userPhone
        self.loc = loc

    def json(self):
        return {
            "userID": self.userID, 
            "userName": self.userName, 
            "userEmail": self.userEmail, 
            "passw": self.passw, 
            "userPhone": self.userPhone, 
            "loc": self.loc
        }

class Child(db.Model):
    __tablename__ = 'child'

    userID = db.Column(db.Integer, db.ForeignKey('user.userID', ondelete="CASCADE"), primary_key=True)
    childName = db.Column(db.String(20), primary_key=True)
    school = db.Column(db.String(100), nullable=False)
    pri = db.Column(db.Boolean, nullable = False)
    lvl = db.Column(db.Integer, nullable=False)
    user = relationship('User', backref='child')

    def __init__(self, userID, childName, school, pri, lvl):
        self.userID = userID
        self.childName = childName
        self.school = school
        self.pri = pri
        self.lvl = lvl
        

    def json(self):
        return {
        "userID": self.userID, 
        "childName": self.childName, 
        "school": self.school, 
        "pri": self.pri, 
        "lvl": self.lvl
        }

class ChildSubjects(db.model):
    __tablename__ = 'childSubjects'

    userID = db.Column(db.Integer, db.ForeignKey('child.userID', ondelete="CASCADE"), primary_key=True)
    childName = db.Column(db.String(20), db.ForeignKey('child.childName', ondelete="CASCADE"), primary_key=True)
    subjects = db.Column(db.String(100), primary_key=True)
    child = relationship('Child', backref='childSubjects')

    def __init__(self, userID, childName, subjects):
        self.userID = userID
        self.childName = childName
        self.subjects = subjects

    def json(self):
        return{
            "userID":self.userID,
            "childName": self.childName,
            "subjects": self.subjects
        }
    

# GET all Users 
@app.route("/user")
def get_all_users():
    userList = User.query.all()
    if len(userList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

# GET User Details By UserID 
@app.route("/user/<string:userID>")
def find_by_UserID(userID):
    userList = User.query.filter_by(userID=userID).first()
    if userList:
        return jsonify(userList.json())
    return jsonify({"message": "User is not found."}), 404

# add new user using POST 
@app.route("/createUser", methods=['POST'])
def add_user():
    data = request.get_json()
    userID = data.userID
    if (User.query.filter_by(userID=userID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userID": userID
                },
                "message": "User already exists."
            }
        ), 400
 
    
    user = User(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID
                },
                "message": "An error occurred creating the User."
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

# check user login
@app.route("/usercheck", methods=['POST', 'GET'])
def check_user():
    data = request.get_json()
    # print(data)
    email = data['userEmail']
    # email= "mikescarn@gmail.com"
    passw = data['passw']
    # passw="helps"
    try:
        res = User.query.filter_by(userEmail=email, passw=passw).first()
        if (res):
            print(res)
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message":"meep",
                        "userID": res.userID,
                        "userName": res.userName,
                        "userEmail": res.userEmail
                    },
                    "message": "User authenticated."
                }
            ), 200
    except Exception as e:

        return jsonify(
            {
                "code": 404,
                "message": "There was an error" + str(e)
            }), 404

# Update user details using UserID --> PUT
@app.route("/editUser/<int:userID>", methods=['PUT'])
def update_user_details(userID):
    try:
        userList = User.query.filter_by(userID=userID).first()
        if not userList:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "userID": userID
                    },
                    "message": "userID has not been updated"
                }
            ), 404

        # update status
        # do for UserPhone and loc 
        data = request.get_json()
        if data['userName']:
            userList.UserName = data['userName']
        if data['userPhone']:
            userList.UserPhone = data['userPhone']
        if data['passw']:
            userList.passw = data['passw']
        if data['loc']:
            userList.loc = data['loc']
        db.session.commit()
            
        return jsonify(
            {
                "code": 200,
                "data": userList.json()
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": userID
                },
                "message": "An error occurred while updating the user. " + str(e)
            }
        ), 500

# GET all children By UserID 
@app.route("/child/<int:userID>")
def find_child_by_user(userID):
    try:
        childList = Child.query.filter_by(userID = userID).all()
        data = []
        if childList:
            for child in childList:
                userID = child['userID']
                childName = child['childName']
                subjects = ChildSubjects.query.filter_by(userID = userID, childName = childName).all()
                child['subjects'] = subjects
                data.append(child)
            return jsonify(
                {
                    "code": 200,
                    "data": data.json()
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "UserID": userID
                },
                "message": "Couldn't find children." + str(e)
            }
        ), 404

# GET Child Details using userid and childName 
@app.route("/seeChild/<int:userID>/<string:childName>")
def find_by_ChildID(userID,childName):
    try:
        childList = Child.query.filter_by(userID = userID, childName = childName).first()
        subject = ChildSubject.query.filter_by(userID = userID, childName = childName).all()
        if childList:
            return jsonify(
                {
                    "code": 200,
                    "childData": childList.json(),
                    "subjectData": subject.json()
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "UserID": userID
                },
                "message": "Couldn't find children." + str(e)
            }
        ), 404

# edit child details from userid and childName 
@app.route("/editChild/<int:userID>/<string:childName>", method=['PUT'])
def edit_by_ChildID(userID,childName):
    try:
        childList = Child.query.filter_by(userID = userID, childName = childName).first()

        data = request.get_json()
        if data['childName']:
            childList.childName = data['childName']
        if data['school']:
            childList.school = data['school']
        if data['pri']:
            childList.school = data['pri']
        if data['lvl']:
            childList.lvl = data['lvl']
        try:
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": childList.json()
                }
            ), 200

        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "UserID": userID
                    },
                    "message": "An error occurred while updating the user. " + str(e)
                }
            ), 500
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "UserID": userID
                },
                "message": "Couldn't find children." + str(e)
            }
        ), 404

# delete child entity
@app.route("/child/<int:userID>/<string:childName>", methods=['DELETE'])
def delete_child(userID, childName):
    try:
        child = Child.query.filter_by(userID=userID, childName=childName).first()
        if child:
            db.session.delete(child)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "childName": childName
                    }
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "childName": childName
                },
                "message": "There was an error deleting the subject." + str(e)
            }
        ), 404



if __name__ =="__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)





