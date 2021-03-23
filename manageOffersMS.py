from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
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
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived offer in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
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

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



def process_offers(offer):
    # 2. Send the order info {cart items}
    # Invoke the order microservice

    ############@EDENA ----HOW TO GET ASSIGNMENT DETAILS AND USE THE ASSIGNMENT DETAILS WHEN CREATING THE OFFER?
    print('\n-----Invoking assignment microservice-----')
    assignment_result = invoke_http(offer_URL, method='GET', json=assignment)
    print('assignment_result:', assignment_result)

    print('\n-----Invoking offer microservice-----')
    offer_result = invoke_http(offer_URL, method='POST', json=offer)
    print('offer_result:', offer_result)

# Check the order result; if a failure, send it to the error microservice.
    code = order_result["code"]
    message = json.dumps(order_result)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (offer error) message with routing_key=offer.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchangename, routing_key="offer.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOffer status ({:d}) published to the RabbitMQ Exchange:".format(
            code), offer_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"offer_result": offer_result},
            "message": "Offer creation failure sent for error handling."
        }

    else:
            
    
    print("\nOrder published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # 5. Send new order to shipping
    # Invoke the shipping record microservice
    print('\n\n-----Invoking inbox microservice-----')

    inbox_result = invoke_http(
        inbox_URL, method="POST", json=offer_result['data'])
    print("inbox_result:", inbox_result, '\n')

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = inbox_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as inbox fails-----')
        print('\n\n-----Publishing the (inbox error) message with routing_key=inbox.error-----')

        # invoke_http(error_URL, method="POST", json=inbox_result)
        message = json.dumps(inbox_result)
        amqpSetup.channel.basic_publish(exchange=amqpSetup.exchangename, routing_key="inbox.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nInbox status ({:d}) published to the RabbitMQ Exchange:".format(
            code), inbox_result)

                # 7. Return error
        return {
            "code": 400,
            "data": {
                "offer_result": offer_result,
                "inbox_result": inbox_result
            },
            "message": "Simulated shipping record error sent for error handling."
        }

    # 7. Return created offer, inbox record
    return {
        "code": 201,
        "data": {
            "offer_result": offer_result,
            "inbox_result": inbox_result
        }
    }

    # Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.