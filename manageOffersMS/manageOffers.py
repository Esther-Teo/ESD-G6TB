from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
sys.path.insert(0, 'C:\wamp64\www\ESD-G6TB')

# HI PLS NOTE!: To run this file without using your local path as seen above^:
    # Navigate into your own local path at GitHub\ESD-G6TB, then type:
    # set PYTHONPATH=.;.\manageOffersMS
    # python manageOffersMS\manageOffers.py

# ALSO: need docker to run amqp stuff (to test in cmd prompt)

from invokes import invoke_http
import amqpSetup

import pika
import json

app = Flask(__name__)
CORS(app)

get_offer_URL = "http://localhost:5001/offerByUser/" # specify userID <int:userID>
create_offer_URL = "http://localhost:5001/createOffer" # creates new offer in assignment.py with POST
create_assignment_URL = "http://localhost:5001/makeAssignment" # creates new assignment in assignment.py with POST 
delete_assignment_URL = "http://localhost:5001/deleteAssignment/" # specify assignmentID to delete: <int:assignmentId>
delete_offer_URL = "http://localhost:5001/deleteOffer/" # specify assignmentId and tutorID: <int:assignmentId>/<int:tutorID>
inbox_URL = "http://localhost:5002/inboxUser/" # specify userID: <int:userID>

#-----------------------------------------------------------------------------------------------------

# Delete Assignments
@app.route("/deleteAssignment", methods=['POST'])
def manage_assignment():
    '''
    User deletes assignment based on assignmentId
    manage_assignment processes JSON request and deletes assignment from assignment table
    '''
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived request in JSON:", offer)

            # Task 2: delete assignment 
            result = delete_assignment(offer)
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
           
#-----------------------------------------------------------------------------------------------------

# User accepts or rejects offer
@app.route("/manageOffers", methods=['POST'])
def manage_offers():
    '''
    User chooses to accept or reject offer
    If reject, manage_offers deletes offer
    If accept, manage_offers creates new assignment, and deletes other offers for that assignment
    '''
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived request in JSON:", offer)

            # Task 3: Accept or Reject Offers
            if offer['acceptOrReject'] == 'accept':
                result = accept_offers(offer)
            elif offer['acceptOrReject'] == 'reject':
                result = reject_offers(offer)

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

#-----------------------------------------------------------------------------------------------------

# Tutor creates offers
@app.route("/tutorOffers", methods=['POST'])
def tutor_creates_offers():
    '''
    Tutor creates new offer and sends info to inbox 
    '''
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived request in JSON:", offer)
            result = create_offer(offer)
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

# Functions for processing
#-----------------------------------------------------------------------------------------------------

# Task 1: Delete assignment based on assignmentId (COMPLETED AND TESTED)
def delete_assignment(offer):
    # if delete == 1, delete. Otherwise, leave it alone
    if offer['delete'] == 1:
        assignmentId = str(offer['assignment']['assignmentId']) 
        print('\n-----Invoking assignmentMS-----')
        deleted_result = invoke_http(delete_assignment_URL + assignmentId, method='DELETE', json=offer)

    return {
        "code": 201,
        "data": {
            "deleted_result": deleted_result,
        }
    }

#-----------------------------------------------------------------------------------------------------

# Task 2a: User accepts offer (NOT TESTED YET)
def accept_offers(offer):
    # If accept, create new assignment, delete other offers for that assignment
    if offer['acceptOrReject'] == 'accept':
        print('\n-----Invoking assignmentMS-----')
        assignment_result = invoke_http(create_assignment_URL, method='POST', json=offer['offer'])

        code = assignment_result["code"] 
        message = json.dumps(assignment_result)
        print('assignment_result', assignment_result)

        if code not in range(200, 300):
            print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
            amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), assignment_result)

            return {
                "code": 500,
                "data": {"offer_result": assignment_result},
                "message": "Inbox failure sent for error handling."
            }  

    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
        }
    }

#-----------------------------------------------------------------------------------------------------

# Task 3: Tutor creates an offer 
def create_offer(offer):
    # POST a new offer 
    print('\n-----Invoking assignmentMS-----') 
    offer_result = invoke_http(create_offer_URL, method='POST', json=offer)

    code = offer_result["code"] 
    message = json.dumps(offer_result)
    print("offer_result", offer_result)

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

        # If successful, send offer to inboxMS
    print('\n-----Sending to inboxMS-----')
    userID = str(offer['userID'])
    inbox_result = invoke_http(inbox_URL + userID, method='POST', json=offer)
    print(inbox_result)
    inbox_code = inbox_result["code"] 
    inbox_message = json.dumps(inbox_result)

    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
            body=inbox_message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(inbox_code), inbox_result)

        return {
            "code": 500,
            "data": {"inbox_result": inbox_result},
            "message": "Inbox failure sent for error handling."
        }  
    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
        }
    }

#-----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing offers...")
    app.run(host="0.0.0.0", port=5100, debug=True)

