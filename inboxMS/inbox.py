# import json
# import os, sys

# sys.path.insert(0, 'c:/Users/foo/Documents/GitHub/ESD-G6TB')
# import amqpSetup

# monitorBindingKey='#'

# def get_inbox_msg():
#     amqpSetup.check_setup()
#     queue_name = "Inbox"  

#     amqpSetup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#     amqpSetup.channel.start_consuming() 

# def callback(channel, method, properties, body): # required signature for the callback; no return
#     print("\nReceived inbox message by " + __file__)
#     process_msg(body)
#     print() 

# def process_msg(inboxMsg):
#     print("Printing inbox message:")
#     try:
#         msg = json.loads(inboxMsg)
#         print("--JSON:", msg)
#     except Exception as e:
#         print("--NOT JSON:", e)
#         print("--DATA:", inboxMsg)
#     print()


# if __name__ == "__main__":  
#     print("\nThis is " + os.path.basename(__file__), end='')
#     print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqpSetup.exchange_name))
#     get_inbox_msg()


#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class RejectedOffer(db.Model):
    __tablename__ = 'rejectedOffer'

    assignmentId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    tutorID = db.Column(db.Integer, nullable=False)
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


@app.route("/inboxUser/<int:userID>", methods=['POST'])
def receiveOrder():
    # Check if the order contains valid JSON
    order = None
    if request.is_json:
        order = request.get_json()
        result = processOrder(order)
        return jsonify(result), result["code"]
    else:
        data = request.get_data()
        print("Received an invalid order:")
        print(data)
        return jsonify({"code": 400,
                        # make the data string as we dunno what could be the actual format
                        "data": str(data),
                        "message": "Order should be in JSON."}), 400  # Bad Request input


def processOrder(order):
    print("Processing an order for shipping:")
    print(order)
    # Can do anything here, but aiming to keep it simple (atomic)
    order_id = order['order_id']
    # If customer id contains "ERROR", simulate failure
    if "ERROR" in order['customer_id']:
        code = 400
        message = 'Simulated failure in shipping record creation.'
    else:  # simulate success
        code = 201
        message = 'Simulated success in shipping record creation.'

    print(message)
    print()  # print a new line feed as a separator

    return {
        'code': code,
        'data': {
            'order_id': order_id
        },
        'message': message
    }



# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5002, debug=True)

