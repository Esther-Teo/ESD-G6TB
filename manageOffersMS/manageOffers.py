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

assignment_URL = "http://localhost:6000/assignmentMS/assignment"
offer_URL = "http://localhost:6001/offerMS/offer"
error_URL = "http://localhost:6002/errorMS/error"
inbox_URL = "http://localhost:6003/inboxMS/inbox"

@app.route("/manageOffersMS", methods=['POST'])
def create_offers():
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived offer in JSON:", order)

            result = process_offers(offer)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "manageOffersMS.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def process_offers(offer):
    ############@EDENA ----HOW TO GET ASSIGNMENT DETAILS AND USE THE ASSIGNMENT DETAILS WHEN CREATING THE OFFER?
    # print('\n-----Invoking assignment microservice-----')
    # assignment_result = invoke_http(offer_URL, method='GET', json=assignment)
    # print('assignment_result:', assignment_result)

    print('\n-----Invoking offer microservice-----')
    offer_result = invoke_http(offer_URL, method='POST', json=offer)
    print('offer_result:', offer_result)

    code = offer_result["code"]
    message = json.dumps(offer_result)

    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as offer fails-----')
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')

        invoke_http(error_URL, method="POST", json=order_result)
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchangename, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
      
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)

        return {
            "code": 500,
            "data": {"offer_result": offer_result},
            "message": "Offer creation failure sent for error handling."
        }            
    
    print("\nOrder published to RabbitMQ Exchange.\n")

    print('\n\n-----Invoking inbox microservice-----')
    inbox_result = invoke_http(inbox_URL, method="POST", json=offer_result['data'])
    print("inbox_result:", inbox_result, '\n')

    code = inbox_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as inbox fails-----')
        print('\n\n-----Publishing the (inbox error) message with routing_key=inbox.error-----')

        invoke_http(error_URL, method="POST", json=inbox_result)
        message = json.dumps(inbox_result)
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchangename, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nInbox status ({:d}) published to the RabbitMQ Exchange:".format(code), inbox_result)

        return {
            "code": 400,
            "data": {
                "offer_result": offer_result,
                "inbox_result": inbox_result
            },
            "message": "Simulated shipping record error sent for error handling."
        }

    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
            "inbox_result": inbox_result
        }
    }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)

