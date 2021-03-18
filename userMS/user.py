from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), nullable=False)
    UserPhone = db.Column(db.Integer, nullable=False)
    Location = db.Column(db.String(100), nullable=False)

    def __init__(self, UserID, UserName, UserPhone, Location):
        self.UserID = UserID
        self.UserName = UserName
        self.UserPhone = UserPhone
        self.Location = Location

    def json(self):
        return {
        "UserID": self.UserID, "UserName": self.UserName, "UserPhone": self.UserPhone, "Location": self.Location
        }

class Child(db.Model):
    __tablename__ = 'child'

    UserID = db.Column(db.Integer, primary_key=True)
    ChildID = db.Column(db.Integer, primary_key=True)
    School = db.Column(db.String(100), nullable=False)
    Level = db.Column(db.String(100), nullable=False)
    Subjects = db.Column(db.String(100), nullable=False)

    def __init__(self, UserID, ChildID, School, Level, Subjects):
        self.UserID = UserID
        self.ChildID = ChildID
        self.School = School
        self.Level = Level
        self.Subjects = Subjects

    def json(self):
        return {
        "UserID": self.UserID, "ChildID": self.ChildID, "School": self.School, "Level": self.Level, "Subjects": self.Subjects
        }


# GET all Users 
@app.route("/user")
def get_all_users():
    userlist = User.query.all()
    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
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
@app.route("/user/<string:UserID>")
def find_by_UserID(UserID):
    userlist = User.query.filter_by(UserID=UserID).first()
    if userlist:
        return jsonify(userlist.json())
    return jsonify({"message": "User is not found."}), 404

# add new user using POST 
@app.route("/user/<string:UserID>", methods=['POST'])
def add_user(UserID):
    if (User.query.filter_by(UserID=UserID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "UserID": UserID
                },
                "message": "User already exists."
            }
        ), 400
 
    data = request.get_json()
    user = User(UserID, **data)
 
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": UserID
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

# Update user details using UserID --> PUT
@app.route("/user/<string:UserID>", methods=['PUT'])
def update_user_details(UserID):
    try:
        userlist = User.query.filter_by(UserID=UserID).first()
        if not userlist:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "UserID": UserID
                    },
                    "message": "UserID has not been updated"
                }
            ), 404

        # update status
        data = request.get_json()
        if data['status']:
            userlist.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": userlist.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "UserID": UserID
                },
                "message": "An error occurred while updating the user. " + str(e)
            }
        ), 500

        # PUT is not working will try to fix it up 
        # will google some shit and fix itup 

        # def put(self, id):
        # user = [user for user in User if user['UserID'] == UserID]

        # if len(user) == 0:
        #     abort(404)

        # user = user[0]

        # # Loop Through all the passed agruments
        # args = self.reqparse.parse_args()
        # for k, v in args.items():
        #     # Check if the passed value is not null
        #     if v is not None:
        #         # if not, set the element in the books dict with the 'k' object to the value provided in the request.
        #         user[k] = v

        # return{"user": marshal(book, bookFields)}

# GET Child details 
@app.route("/user/child")
def get_child():
    childlist = Child.query.all()
    if len(childlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Child": [child.json() for child in childlist]
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
@app.route("/user/<string:UserID>/<string:ChildID>")
def find_by_ChildID(UserID,ChildID):
    childlist = Child.query.filter_by(UserID = UserID, ChildID = ChildID).first()
    if childlist:
        return jsonify(childlist.json())
    return jsonify({"message": "Child is not found."}), 404


if __name__ =="__main__":
    app.run(port=5000, debug=True)





