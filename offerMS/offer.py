from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/offer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Offer(db.Model):
    __tablename__ = 'offer'
 
    assignmentid = db.Column(db.Integer, primary_key=True)
    tutorid = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(6), nullable=False)
    selectedtime = db.Column(db.Integer, nullable=False)
    offeredrate = db.Column(db.Integer, nullable=False)
    selectedday = db.Column(db.String(3), nullable=False)
 
    def __init__(self, assignmentid, tutorid, status, selectedtime, offeredrate, selectedday):
        self.assignmentid = assignmentid
        self.tutorid = tutorid
        self.status = status
        self.selectedtime = selectedtime
        self.offeredrate = offeredrate
        self.selectedday = selectedday
 
    def json(self):
        return {"assignmentid": self.assignmentid, "tutorid": self.tutorid, "status": self.status, "selectedtime": self.selectedtime, "offeredrate": self.offeredrate, "selectedday": self.selectedday,}

@app.route("/offer")
def get_all():
	offerlist = Offer.query.all()
	if len(offerlist):
		return jsonify(
            {
                "code": 200,
                "data": {
                    "offers": [offer.json() for offer in offerlist]
                }
            }
        )
	return jsonify(
		{
            "code": 404,
            "message": "There are no offers."
        }
    ), 404

 
@app.route("/offer/<int:assignmentid>/<int:tutorid>")
def find_by_pk(assignmentid, tutorid):
	offer = Offer.query.filter_by(assignmentid=assignmentid, tutorid=tutorid).first()
	if offer:
		return jsonify(
            {
                "code": 200,
                "data": offer.json()
            }
        )
	return jsonify(
        {
            "code": 404,
            "message": "Offer not found."
        }
    ), 404

 
@app.route("/offer/<int:assignmentid>/<int:tutorid>", methods=['POST'])
def create_offer(assignmentid, tutorid):
	if (Offer.query.filter_by(assignmentid=assignmentid, tutorid=tutorid).first()):
		return jsonify(
            {
                "code": 400,
                "data": {
                    "assignmentid": assignmentid, 
					"tutorid": tutorid
                },
                "message": "Offer already exists."
            }
        ), 400
 
	data = request.get_json()
	offer = Offer(assignmentid, tutorid, **data)
 
	try:
		db.session.add(offer)
		db.session.commit()
	except:
		return jsonify(
            {
                "code": 500,
                "data": {
                    "assignmentid": assignmentid,
                    "tutorid": tutorid
                },
                "message": "An error occurred creating the offer."
            }
        ), 500
 
	return jsonify(
        {
            "code": 201,
            "data": offer.json()
        }
    ), 201

 
if __name__ == '__main__':
    app.run(port=5003, debug=True)