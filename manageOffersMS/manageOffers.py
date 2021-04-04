from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
sys.path.insert(0, 'c:/Users/foo/Documents/GitHub/ESD-G6TB')
# To run this file without using your local path as seen above^:
    # Navigate into your own local path at GitHub\ESD-G6TB, then type:
    # set PYTHONPATH=.;.\manageOffersMS
    # python manageOffersMS\manageOffers.py

from invokes import invoke_http
import amqpSetup

import pika
import json

app = Flask(__name__)
CORS(app)

assignment_URL = "http://localhost:5001/assignment"
offer_URL = "http://localhost:5003/offer"
createOffer_URL = "http://localhost:5001/createOffer"

# Manage a new offer
@app.route("/manageOffersMS", methods=['POST'])
def manage_offers():
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived offer in JSON:", offer)
            # 2. User views offer
            result = process_offers(offer)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "manageOffersMS.py internal error: " + ex_str
            }), 500
    # Not in JSON format
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# _______________________________________________________________________________________________________

def process_offers(offer):
    # 3. Get offer details 
    print('\n-----Invoking assignmentMS-----')
    offer_result = invoke_http(createOffer_URL, method='POST', json=offer)
    print('offer_result:', offer_result)

    code = offer_result["code"] 
    message = json.dumps(offer_result)

    # If error, send to error handler
    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
      
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)

        return {
            "code": 500,
            "data": {"offer_result": offer_result},
            "message": "Offer creation failure sent for error handling."
        }            
    
    else:
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print("\nOrder published to RabbitMQ Exchange.\n")

    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
            # "inbox_result": inbox_result
        }
    }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing offers...")
    app.run(host="0.0.0.0", port=5100, debug=True)

