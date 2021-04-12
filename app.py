import os
import json 
import stripe
import random
import string
import logging  
# from dotenv import load_dotenv, find_dotenv

from flask import Flask, jsonify, request, render_template, url_for , redirect , session , send_from_directory, Response
from flask_cors import CORS


app = Flask(__name__)
# using testing environment
CORS(app)

#ALL CONFIG
# Stripe config  
app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51Ib4VfBvhmRsAY8LWdqkxz5jziPQ1YmxCjuFHuQCaJyMNjoJSipniNaC1lh9ZocTLnpaxVWwgKkFSeX76ACHNqZP007ogKEoHo",
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn',
app.config['STRIPE_WEBHOOK_SECRET'] = "whsec_UixySdHiQLuh62bwkQiVxWBupQ2j9skd"

# use secret key in the app

PUBLIC='pk_test_51Ib4VfBvhmRsAY8LWdqkxz5jziPQ1YmxCjuFHuQCaJyMNjoJSipniNaC1lh9ZocTLnpaxVWwgKkFSeX76ACHNqZP007ogKEoHo'
SECRET='sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'
WEBHOOK='whsec_UixySdHiQLuh62bwkQiVxWBupQ2j9skd'
stripe.api_key = 'sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'

# This enables Flask sessions. it's random u can put some random stuff for flask session. 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#not used
# START OF BUY
# method with sessions
@app.route('/')
def index():
    return render_template('checkout.html')

# this is for one time checkout basically for buy books from the platform but that would be too simple. Hence we are implementing stripe connect to facilitate P2P payments
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # Creating a session upon load
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": "price_1Ib4ZZBvhmRsAY8LTTWPEqWj",
                "quantity": 1,
            },
        ],
        # line items are what the customer will be paying for.
        # line_items[price] is retrieved from the product ID in stripe
        mode="payment",
        success_url=url_for('success', _external=True) + '?session_id={checkout_session_id}',
        cancel_url=url_for('index', _external=True),
    )
    return jsonify(id=session.id)

#not used 
@app.route('/success.html')
def success():
    return render_template('success.html')
# END OF BUY SHIT 

#ONBOARDING 
#An email address associated with the account. You can treat this as metadata: it is not used for authentication or messaging account holders.
# fix email to stripe account.
@app.route('/onboard-user', methods=['GET','POST'])
def onboard_user():
    data = json.loads(request.data)
    print(data)
    user_email=data['userEmail']
    print(f"Data passed is: {user_email}")
    account = stripe.Account.create(country='SG',type='custom', email=user_email,
     capabilities={
    'card_payments': {
      'requested': True,
    },
    'transfers': {
      'requested': True,
    },
    'bancontact_payments': {
      'requested': True,
    },
    'eps_payments': {
      'requested': True,
    },
    'giropay_payments': {
      'requested': True,
    },
    'ideal_payments': {
      'requested': True,
    },
    'p24_payments': {
    'requested': True,
    },
    'sepa_debit_payments': {
    'requested': True,
    },
    'sofort_payments': {
    'requested': True,
    }
  })
    # Store the account ID.

    print(account)
    session['account_id'] = account.id

    origin = request.headers['origin']
    account_link_url = _generate_account_link(account.id, origin)
    try:
        return jsonify({'url': account_link_url})
    except Exception as e:
        return jsonify(error=str(e)), 403

# route here after clicking the connect button 
# Sessions for users when they redirect 
@app.route('/onboard-user/refresh', methods=['GET'])
def onboard_user_refresh():
    if 'account_id' not in session:
        return redirect('/')
    account_id = session['account_id']

    origin = ('https://' if request.is_secure else 'http://') + request.headers['host']
    print(origin)
    account_link_url = _generate_account_link(account_id, origin)
    return redirect(account_link_url)



def _generate_account_link(account_id, origin):
    #edene here! edit the return URL to yours. orgin refers to localhost or wat u set docker to be e.g 127.0.0.1 or anything
    print(f'account id in generatelink is {account_id}')
    account_link = stripe.AccountLink.create(

        type='account_onboarding',
        account=account_id,
        collect='eventually_due',
        refresh_url=f'http://127.0.0.1:5000/onboard-user/refresh',
        # return_url=f'{origin}/ESD/ESD-G6TB/app/templates/registerPage.html',
        # this is my localhost. 
        return_url=f'C:\wamp64\www\213\ESD\Project\template\app\ESD-G6TB\app\templates\registerTutorFallback.html' + '?accountid='+account_id,
        # return_url=f'{origin}:5000/app/templates/registerTutorFallback.html' + '?accountid='+account_id,

    )
    # print(origin)
    print(account_link.url)
    return account_link.url



# END OF ONBOARDING 


# Start of Connect Pay 
# this is for parents to pay the tutors
@app.route('/connect_pay.html', methods=['GET'])
def connect_pay():
    return render_template('connect_pay.html')


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    # print(items)
    # [{'id': 'private_tuition', 'amount': 700}]
    charge_per_hour=items[0]["amount"]
    # multiply by 3 hours 
    charge_per_hour = charge_per_hour * 3 
    print(charge_per_hour)
    return charge_per_hour


def calculate_application_fee_amount(amount):
    # Take a 5% cut.
    return int(.05 * amount)


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    # returns the server calculated amount in 2 functions above 
    amount = calculate_order_amount(data['items'])
    print(data['account'])
    # Create a PaymentIntent with the order amount, currency, and transfer destination
    intent = stripe.PaymentIntent.create(
        amount=amount,
        # currency in SGD 
        currency=data['currency'],
        transfer_data={'destination': data['account']},
        application_fee_amount=calculate_application_fee_amount(amount)
    )

    try:
        # Send publishable key and PaymentIntent details to client
        # handle_successful_payment_intent(intent)
        return jsonify({'publishableKey': PUBLIC, 'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403

# this calls my all connected account to my stripe connect currently theres one
@app.route("/recent-accounts", methods=["GET"])
def get_accounts():
    accounts = stripe.Account.list(limit=100)
    return jsonify({'accounts': accounts})

# fix this 
@app.route("/express-dashboard-link", methods=["GET"])
def get_express_dashboard_link():
    account_id = request.args.get('account_id')
    link = stripe.Account.create_login_link(account_id, redirect_url=(request.url_root))
    # this link is the one saved in the platform account. 
    return jsonify({'url': link.url})


# track user with web hook. leave the web hook alone first 
@app.route("/webhook", methods=["POST"])
def webhook_received():
  payload = request.get_data()
  # Signature by stripe endpoint. 
  signature = request.headers.get("stripe-signature")
  print(signature)

  # Verify webhook signature and extract the event. The webhook used is set up to my account 
  # See https://stripe.com/docs/webhooks/signatures for more information.
  try:
    event = stripe.Webhook.construct_event(
        payload=payload, sig_header=signature, secret=WEBHOOK
    )
  except ValueError as e:
    # Invalid payload.
    print(e)
    return Response(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid Signature.
    print(e, signature, os.getenv('STRIPE_WEBHOOK_SECRET'), payload)
    return Response(status=400)

  if event["type"] == "payment_intent.succeeded":
    payment_intent = event["data"]["object"]
    # handle_successful_payment_intent(payment_intent)
    print('runs under webhook?')
    #Send to broker here 


  return json.dumps({"success": True}), 200



# rabbitMQ commented out first it works but my docker has some problems rn.
#   
# @app.route("/send-payment-to-rabbit", methods=["POST"])
# def handle_successful_payment_intent():

#     print("runs after payment")
#     data = json.loads(request.data)
#     message=json.dumps(data)
#     print(message)
#     amqp_setup2.channel.basic_publish(exchange=amqp_setup2.exchangename, routing_key="payment_successful", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2))
#     return json.dumps({"success": True}), 200


# @ramq.queue(exchange_name='payment_exchange', routing_key='flask_rabmq.fail')
# def broker_successful_payment_intent(payment_intent):
#     if amqp_setup.channel.basic_public(exchange=amqp_setup.exchangename, routing_key="pay_successful")




if __name__ == '__main__':
    # ramq.run_consumer()

    app.run(debug=True, port=5007)





## Payment intent object 
# {
#   "id": "pi_1IcTHFBvhmRsAY8L4bBlSj27",
#   "object": "payment_intent",
#   "amount": 1400,
#   "amount_capturable": 0,
#   "amount_received": 0,
#   "application": null,
#   "application_fee_amount": 140,
#   "canceled_at": null,
#   "cancellation_reason": null,
#   "capture_method": "automatic",
#   "charges": {
#     "object": "list",
#     "data": [],
#     "has_more": false,
#     "url": "/v1/charges?payment_intent=pi_1IcTHFBvhmRsAY8L4bBlSj27"
#   },
#   "client_secret": "pi_1IcTHFBvhmRsAY8L4bBlSj27_secret_gWq5uADpap6kVhAW8ZqcTFCQz",
#   "confirmation_method": "automatic",
#   "created": 1617532437,
#   "currency": "usd",
#   "customer": null,
#   "description": null,
#   "invoice": null,
#   "last_payment_error": null,
#   "livemode": false,
#   "metadata": {},
#   "next_action": null,
#   "on_behalf_of": null,
#   "payment_method": null,
#   "payment_method_options": {
#     "card": {
#       "installments": null,
#       "network": null,
#       "request_three_d_secure": "automatic"
#     }
#   },
#   "payment_method_types": [
#     "card"
#   ],
#   "receipt_email": null,
#   "review": null,
#   "setup_future_usage": null,
#   "shipping": null,
#   "statement_descriptor": null,
#   "statement_descriptor_suffix": null,
#   "status": "requires_payment_method",
#   "transfer_data": {
#     "destination": "acct_1Ic8ngAiyPfscIUT"
#   },
#   "transfer_group": null
# }
