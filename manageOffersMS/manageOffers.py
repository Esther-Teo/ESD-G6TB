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

# assignment_URL = "http://localhost:5001/assignment"
# offer_URL = "http://localhost:5003/offer"

get_offer_URL = "http://localhost:5001/offerByUser/" # specify userID <int:userID>
create_offer_URL = "http://localhost:5001/createOffer" # creates new offer in assignment.py with POST
create_assignment_URL = "http://localhost:5001/makeAssignment" # creates new assignment in assignment.py with POST 
delete_assignment_URL = "http://localhost:5001/deleteAssignment/" # specify assignmentID to delete: <int:assignmentId>
delete_offer_URL = "http://localhost:5001/deleteOffer/" # specify assignmentId and tutorID: <int:assignmentId>/<int:tutorID>

# Routing
#-----------------------------------------------------------------------------------------------------

# Get all offers 
@app.route("/getUserOffers", methods=['GET'])
def get_user_offers():
    if request.is_json:
        try:
            offer = request.get_json()
            print("\nReceived request in JSON:", offer)

            # Task 1: Get offers for a user
            result = get_offers(offer)
            print('\n------------------------')
            print('\nresult: ', result)
            # return jsonify(result), result["code"]
            return jsonify(result)

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

# Manage Assignments
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

# Manage offer (has error)
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

# Functions for processing
#-----------------------------------------------------------------------------------------------------

def get_offers(offer):
    userID = str(offer['userID'])
    print('\n-----Invoking assignmentMS-----')
    offer_result = invoke_http(get_offer_URL + userID, method='GET', json=offer)

    code = offer_result["code"] 
    message = json.dumps(offer_result)
    print('offer_result', offer_result)

    # Error handling
    if code not in range(200, 300):
        print('\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)

        return {
            "code": 500,
            "data": {"offer_result": message},
            "message": "Offers failure sent for error handling."
        }

    # If no error, send deletion results to inbox
    else:
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print("\nMessage published to RabbitMQ Exchange.\n")
    # Return success code 
    return {
        "code": 201,
        "data": {
            "offer_result": offer_result
        }
    }

#-----------------------------------------------------------------------------------------------------

# Task 2: Delete assignment from assignment.sql, send {code, message} to inbox as amqp if successful 
def delete_assignment(offer):
    # if delete == 1, delete. Otherwise, leave it alone
    if offer['delete'] == 1:
        assignmentId = str(offer['assignment']['assignmentId']) 
        print('\n-----Invoking assignmentMS-----')
        deleted_result = invoke_http(delete_assignment_URL + assignmentId, 
                    method='DELETE', json=offer['assignment'])

        code = deleted_result["code"] 
        message = json.dumps(deleted_result)
        print('deleted_result', deleted_result)
        if deleted_result:
            print("------Assignment", assignmentId, "has been deleted------")

    else: 
        return None

    # Error handling
    if code not in range(200, 300):
        print('\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), deleted_result)

        return {
            "code": 500,
            "data": {"deleted_result": message},
            "message": "Please specify assignmentId to delete assigment."
        }

    # If no error, send deletion results to inbox
    else:
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print("\nMessage published to RabbitMQ Exchange.\n")
    # Return success code 
    return {
        "code": 201,
        "data": {
            "deleted_result": deleted_result,
        }
    }

#-----------------------------------------------------------------------------------------------------

# Task 3a: User accepts offer 
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
                "message": "Acceptance/rejection failure sent for error handling."
            }   
        
    else:
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    print("\nMessage published to RabbitMQ Exchange.\n")

    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
        }
    }

#-----------------------------------------------------------------------------------------------------

# Task 3b: User rejects offer 
def reject_offers(offer):
    # If reject, delete offer and send {code, message} to inbox 
    if offer['acceptOrReject'] == 'reject':
        assignmentId = str(offer['offer']['assignmentId'])
        tutorID = '/' + str(0) 
        print('\n-----Invoking assignmentMS-----')
        offer_result = invoke_http(delete_offer_URL + assignmentId + tutorID, 
                    method='DELETE', json=offer)

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
                "message": "Rejection failure sent for error handling."
            }   
        
    else:
        print('\n\n-----Publishing the (offer info) message with routing_key=offer.inbox-----') 
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchange_name, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    print("\nMessage published to RabbitMQ Exchange.\n")

    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
        }
    }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing offers...")
    app.run(host="0.0.0.0", port=5100, debug=True)

