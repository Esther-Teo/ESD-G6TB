from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
# sys.path.insert(0, 'C:\GitHub\ESD-G6TB')

# HI PLS NOTE!: To run this file without using your local path as seen above^: NOT NEEDED ANYMORE
    # Navigate into your own local path at GitHub\ESD-G6TB, then type:
    # set PYTHONPATH=.;.\manageOffersMS
    # python manageOffer

# ALSO: need docker to run amqp stuff (to test in cmd prompt)

from invokes import invoke_http
import amqp_setup

import pika
import json

app = Flask(__name__)
CORS(app)

# Assignment
get_offer_URL = "http://assignment:5001/offerByUser/" # GETS offer (<int:userID>)
get_offer_by_assignment_URL = "http://assignment:5001/offerByAssignment/" # GET offer (<int:assignmentId>)
create_offer_URL = "http://assignment:5001/createOffer" # POST new offer 
reject_offer_URL = "http://assignment:5001/rejectOffer/" # DELETE offer (<int:assignmentId>/<int:tutorID>)
accept_offer_URL = "http://assignment:5001/acceptOffer/" # PUT assignment (<int:assignmentId>/<int:tutorID>)

update_assignment_URL = "http://assignment:5001/assignment/" # PUT assignment (<int:assignmentId>)
create_assignment_URL = "http://assignment:5001/makeAssignment" # POST new assignment 
delete_assignment_URL = "http://assignment:5001/deleteAssignment/" # DELETE assignment (<int:assignmentId>)

# Inbox
inbox_create_offer_URL = "http://inbox:5002/createOffer" # POST new offer to USER
inbox_return_offer_URL = "http://inbox:5002/returnOffer" # POST accepted/rejected offer to TUTOR 

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
            # Delete assignment 
            if offer['delete'] == 1:
                result = delete_assignment(offer)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            return jsonify({"code": 500, "message": "manageOffersMS.py internal error: " + ex_str}), 500
    return jsonify({"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}), 400   
           
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
            # Accept or Reject Offers
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
            return jsonify({"code": 500, "message": "manageOffersMS.py internal error: " + ex_str}), 500
    return jsonify({"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}), 400   

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
            return jsonify({"code": 500, "message": "manageOffersMS.py internal error: " + ex_str}), 500
    return jsonify({"code": 400, "message": "Invalid JSON input: " + str(request.get_data())}), 400

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Functions for processing
#-----------------------------------------------------------------------------------------------------
# Task 0: Delete assignment based on assignmentId (COMPLETED, TEST SUCCESSFUL) 
def delete_assignment(offer):
    # for each offer, reject using reject_offers 
    # reject_offers: changes status to rejected and sends to returnedoffer in inbox.sql
    assignmentId = str(offer['assignment']['assignmentId']) 
    print('-------------------------REJECTING OFFERS-------------------------')  
    all_offers = invoke_http(get_offer_by_assignment_URL + assignmentId, method='GET', json=offer)
    temp = {}  
    for offer in all_offers['offers']:
        temp['offer'] = offer
        print(reject_offers(temp))

    print('\n-----Invoking assignmentMS-----')
    deleted_result = invoke_http(delete_assignment_URL + assignmentId, method='DELETE', json=offer)
    code = deleted_result["code"] 
    message = json.dumps(deleted_result)
    print('deleted_result:', deleted_result)

    # Error handling
    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="assignment.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), deleted_result)
        return {"code": 500, "data": {"deleted_result": deleted_result}, "message": "Assignment deletion failure sent for error handling."}

    return {"code": 201, "data": {"deleted_result": deleted_result}}

#-----------------------------------------------------------------------------------------------------
# Task 1: User rejects offer (COMPLETED, TEST SUCCESSFUL) 
def reject_offers(offer):
    # Change status of offer to 'rejected'
    print('\n-----Invoking assignmentMS-----')
    assignmentId = str(offer['offer']['assignmentId'])
    tutorID = '/' + str(offer['offer']['tutorID'])
    offer_result = invoke_http(reject_offer_URL + assignmentId + tutorID, method='PUT', json=offer['offer'])
    code = offer_result["code"] 
    message = json.dumps(offer_result)
    print('offer_result:', offer_result)

    # Error handling
    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)
        return {"code": 500, "data": {"offer_result": offer_result}, "message": "Offer creation failure sent for error handling."}
   
    # send rejected offer to returnedoffer table 
    print('-----Offer has been rejected-----')
    print('-----Sending Rejected Offer to Inbox-----')
    new = {"offer": offer_result['data']}
    inbox_result = invoke_http(inbox_return_offer_URL, method='POST', json=new)
    inbox_code = inbox_result["code"] 
    inbox_message = json.dumps(inbox_result)
    print('inbox_result:', inbox_result)

    # Error handling
    if inbox_code not in range(200, 300):
        print('\n\n-----Publishing the (inbox error) message with routing_key=inbox.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="inbox.error", 
            body=inbox_message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(inbox_code), inbox_result)
        return {"code": 500, "data": {"inbox_result": inbox_result}, "message": "Inbox failure sent for error handling."}  

    # Return offer if no errors
    return {"code": 201, "data": { "offer_result": offer_result}}
#-----------------------------------------------------------------------------------------------------
# Task 2: User accepts offer (COMPLETED, TEST SUCCESSFUL)
def accept_offers(offer):
    # change offer status to 'accepted'
    print('\n-----Invoking assignmentMS-----')
    assignmentId = str(offer['offer']['assignmentId'])
    tutorID = '/' + str(offer['offer']['tutorID'])
    offer_result = invoke_http(accept_offer_URL + assignmentId + tutorID, method='PUT', json=offer['offer'])
    code = offer_result["code"] 
    message = json.dumps(offer_result)
    print('offer_result:', offer_result)

    # Error handling for changing offer status 
    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)
        return {"code": 500,"data": {"offer_result": offer_result},"message": "Offer failure sent for error handling."}  

    # send accepted offer to returnedoffer table in inbox.sql
    print('-----Sending to Accepted offer to Inbox-----')
    new = {"offer": offer_result['data']}
    inbox_result = invoke_http(inbox_return_offer_URL, method='POST', json=new)
    inbox_code = inbox_result["code"] 
    inbox_message = json.dumps(inbox_result)
    print("inbox_result", inbox_result)

    # Error handling for sending accepted offer 
    if inbox_code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=inbox.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="inbox.error", 
            body=inbox_message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(inbox_code), inbox_result)
        return {"code": 500,"data": {"inbox_result": inbox_result},"message": "Inbox failure sent for error handling."}

    # for each offer, reject using reject_offers 
    # reject_offers: changes status to rejected and sends to returnedoffer in inbox.sql
    print('-------------------------REJECTING OFFERS-------------------------')    
    all_offers = invoke_http(get_offer_by_assignment_URL + assignmentId, method='GET', json=offer['offer'])
    temp = {}
    accepted_offer = offer_result['data']
    for rej_offer in all_offers['offers']: 
        if rej_offer != accepted_offer:
            temp['offer'] = rej_offer
            print(reject_offers(temp))

    # change the tutorID in assignment table to match the accepted offer 
    print('-----Updating TutorID in Assignment-----')
    update = invoke_http(update_assignment_URL + assignmentId, method='PUT', json=offer['offer'])
    update_code = update["code"] 
    update_message = json.dumps(update)
    print("Update Assignment Results:", update)

    # Error handling
    if update_code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=inbox.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="inbox.error", 
            body=update_message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(update_code), update)
        return {"code": 500,"data": {"updated assignment": update},"message": "Inbox failure sent for error handling."}

    return {"code": 201,"data": {"offer_result": offer_result}}

#-----------------------------------------------------------------------------------------------------
# Task 3: Tutor creates an offer (COMPLETED, TEST SUCCESSFUL) 
def create_offer(offer):
    # POST a new offer 
    print('\n-----Invoking assignmentMS-----') 
    offer_result = invoke_http(create_offer_URL, method='POST', json=offer)
    code = offer_result["code"] 
    message = json.dumps(offer_result)
    print("offer_result", offer_result)

    # Error handling
    if code not in range(200, 300):
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(code), offer_result)
        return {"code": 500, "data": {"offer_result": offer_result}, "message": "Offer creation failure sent for error handling."}

    # If successful, send offer to inboxMS
    print('\n-----Sending to inboxMS-----')
    inbox_result = invoke_http(inbox_create_offer_URL, method='POST', json=offer)
    inbox_code = inbox_result["code"] 
    inbox_message = json.dumps(inbox_result)
    print("inbox_result", inbox_result)

    # Error handling
    if inbox_code not in range(200, 300):
        print('\n\n-----Publishing the (inbox error) message with routing_key=inbox.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="inbox.error", 
            body=inbox_message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(inbox_code), inbox_result)
        return {"code": 500, "data": {"inbox_result": inbox_result}, "message": "Inbox failure sent for error handling."}  

    # Return offer if no errors
    return {"code": 201, "data": { "offer_result": offer_result}}

#-----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing offers...")
    app.run(host="0.0.0.0", port=5100, debug=True)

