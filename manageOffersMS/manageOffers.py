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
create_offer_URL = "http://localhost:5001/createOffer" # creates new offer in assignment.py
delete_offer_URL = "http://localhost:5001/deleteAssignment/" # specify assignmentID to delete: <int:assignmentId>

# Manage a new offer
@app.route("/manageOffersMS", methods=['POST'])
def manage_offers():
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived request in JSON:", offer)
            # Task 1: delete assignment
            
            delete_result = delete_assignment(offer)
            print('\n------------------------')
            print('\nresult: ', delete_result)
            return jsonify(delete_result), delete_result["code"]
            # Task 2: (to be done)
            # if  
            #     process_result = process_offers(offer)
            # print('\n------------------------')
            # print('\nresult: ', result)
            # return jsonify(result), result["code"]

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

# Task 1: Delete assignment 
def delete_assignment(offer):
    # if delete == 1, delete. Otherwise, leave it alone
    if offer['delete'] == 1:
        assignmentId_to_delete = offer['offer']['assignmentId'] 
        print('\n-----Invoking assignmentMS-----')
        deleted_result = invoke_http(delete_offer_URL + str(assignmentId_to_delete), method='DELETE', json=offer['offer'])

        code = deleted_result["code"] 
        message = json.dumps(deleted_result)
    else:
        return None

    # Error handling
    if code not in range(200, 300):
        print('\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), delete_result)

        return {
            "code": 500,
            "data": {"deleted_result": deleted_result},
            "message": "Deletion failure sent for error handling."
        }

    # If no error, send deletion results to inbox
    else:
        print("-----Assignment", str(assignmentId_to_delete), "has been deleted-----")
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print("\nOrder published to RabbitMQ Exchange.\n")
    # Return success code 
    return {
        "code": 201,
        "data": {
            "deleted_result": deleted_result,
        }
    }

# Task 2: (to be done)
def process_offers(offer):
    print('\n-----Invoking assignmentMS-----')
    offer_result = invoke_http(create_offer_URL, method='POST', json=offer)
    print('offer_result:', offer_result)

    code = offer_result["code"] 
    message = json.dumps(offer_result)

    # Error handling
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
        }
    }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing offers...")
    app.run(host="0.0.0.0", port=5100, debug=True)

