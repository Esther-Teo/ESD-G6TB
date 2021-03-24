from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
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
    password = db.Column(db.String(20), nullable=False)
    userPhone = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __init__(self, userID, userName, userEmail, password,  userPhone, location):
        self.userID = userID
        self.userName = userName
        self.userEmail = userEmail
        self.password = password
        self.userPhone = userPhone
        self.location = location

    def json(self):
        return {
        "userID": self.userID, "userName": self.userName, "userEmail": self.userEmail, "password": self.password, "userPhone": self.userPhone, "location": self.location
        }

class Child(db.Model):
    __tablename__ = 'child'

    userID = db.Column(db.Integer, primary_key=True)
    childID = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(100), nullable=False)
    primary = db.Column(db.Boolean, nullable = False)
    secondary = db.Column(db.Boolean, nullable = False)
    level = db.Column(db.String(100), nullable=False)
    subjects = db.Column(db.String(100), nullable=False)

    def __init__(self, userID, childID, school, primary, secondary, level, subjects):
        self.userID = userID
        self.childID = childID
        self.school = school
        self.level = level
        self.subjects = subjects

    def json(self):
        return {
        "userID": self.userID, "childID": self.childID, "school": self.school, "level": self.level, "subjects": self.subjects
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
 
    
    user = User(userID, **data)
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
    # email = data.userEmail;
    email= "mikescarn@gmail.com"
    # passw = data.password;
    passw="helps"
    try:
        if (User.query.filter_by(userEmail=email, password=passw).first()):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "message":"meep"
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
@app.route("/user/<string:userID>", methods=['PUT'])
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
        # do for UserPhone and Location 
        data = request.get_json()
        if data['userPhone']:
            userList.UserPhone = data['userPhone']
        if data['location']:
            userList.location = data['location']
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



# GET Child details 
@app.route("/user/child")
def get_child():
    childList = Child.query.all()
    if len(childList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Child": [child.json() for child in childList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no child."
        }
    ), 404

# GET Child Details using ChildID 
@app.route("/user/<string:userID>/<string:childID>")
def find_by_ChildID(userID,childID):
    childList = Child.query.filter_by(userID = userID, childID = childID).first()
    if childList:
        return jsonify(childList.json())
    return jsonify({"message": "child is not found."}), 404


if __name__ =="__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)





