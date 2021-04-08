import os
import json 
import stripe
import random
import string

# i don't think i need send for directory?? Use it later when deploying live. 
# from dotenv import load_dotenv, find_dotenv
#dotenv is for env file. Keys are hardcoded first. configure later. 
from flask import Flask, jsonify, request, render_template, url_for , redirect , session , send_from_directory, Response
from flask_cors import CORS
# r = requests.get('https://httpbin.org/get')
# print(r.status_code)

app = Flask(__name__)
# test='sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'
# tess='sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'
# using testing environment
CORS(app)
app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51Ib4VfBvhmRsAY8LWdqkxz5jziPQ1YmxCjuFHuQCaJyMNjoJSipniNaC1lh9ZocTLnpaxVWwgKkFSeX76ACHNqZP007ogKEoHo",
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn',
app.config['STRIPE_WEBHOOK_SECRET'] = "whsec_UixySdHiQLuh62bwkQiVxWBupQ2j9skd"
# config is an object for flask
# The config is actually a subclass of a dictionary and can be modified just like any dictionary

# use secret key in the app

PUBLIC='pk_test_51Ib4VfBvhmRsAY8LWdqkxz5jziPQ1YmxCjuFHuQCaJyMNjoJSipniNaC1lh9ZocTLnpaxVWwgKkFSeX76ACHNqZP007ogKEoHo'
SECRET='sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'
WEBHOOK='whsec_UixySdHiQLuh62bwkQiVxWBupQ2j9skd'
# wtf app.config dont work?? 
# stripe.api_key = app.config['STRIPE_SECRET_KEY']
stripe.api_key = 'sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'



# This enables Flask sessions. it's random u can put some random stuff for flask session. 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



# START OF BUY SHIT 
# method with sessions
@app.route('/')
def index():

    return render_template('checkout.html')



# this is for one time checkout basically for buy books from the platform
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


@app.route('/success.html')
def success():
    return render_template('success.html')
# END OF BUY SHIT 

#ONBOARDING 

@app.route('/onboard-user', methods=['GET','POST'])
def onboard_user():
    account = stripe.Account.create(type='standard')
    # Store the account ID.
    print(account.id)
    session['account_id'] = account.id

    origin = request.headers['origin']
    account_link_url = _generate_account_link(account.id, origin)
    try:
        return jsonify({'url': account_link_url})
    except Exception as e:
        return jsonify(error=str(e)), 403

# route here after clicking the connect button 
# SESSIONS WHEN USERS REFRESH LIKE A FKER USERS ARE 
@app.route('/onboard-user/refresh', methods=['GET'])
def onboard_user_refresh():
    if 'account_id' not in session:
        return redirect('/')
    # wdym session not define fk u
    account_id = session['account_id']

    origin = ('https://' if request.is_secure else 'http://') + request.headers['host']
    print(origin)
    account_link_url = _generate_account_link(account_id, origin)
    return redirect(account_link_url)



def _generate_account_link(account_id, origin):
    print(origin)
    account_link = stripe.AccountLink.create(
        type='account_onboarding',
        account=account_id,
        # refresh_url=f'{origin}/onboard-user/refresh',
        # return_url=f'{origin}/success.html',
        
        # refresh_url=f'{origin}/onboard-user/refresh',
        refresh_url=f'http://127.0.0.1:5000/onboard-user/refresh',
        return_url=f'{origin}/ESD/ESD-G6TB/app/templates/registerPage.html',
   
    )
    print(origin)
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

    #from json file but hardcoded first to $65
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
    # returns the hardcoded amount in 2 functions above 
    amount = calculate_order_amount(data['items'])

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
        return jsonify({'publishableKey': PUBLIC, 'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403

# this calls my all connected account to my stripe connect currently theres one
@app.route("/recent-accounts", methods=["GET"])
def get_accounts():
    accounts = stripe.Account.list(limit=10)
    return jsonify({'accounts': accounts})


@app.route("/express-dashboard-link", methods=["GET"])
def get_express_dashboard_link():
    account_id = request.args.get('account_id')
    link = stripe.Account.create_login_link(account_id, redirect_url=(request.url_root))
    # this link is the one saved in the platform account. 
    return jsonify({'url': link.url})


# track user with web hook. 
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
    handle_successful_payment_intent(payment_intent)

  return json.dumps({"success": True}), 200


def handle_successful_payment_intent(payment_intent):
  # dump the response. 
  # configure to some sucess page 
  print('PaymentIntent: ' + str(payment_intent))
  



if __name__ == '__main__':

    app.run(debug=True, port=5006)
