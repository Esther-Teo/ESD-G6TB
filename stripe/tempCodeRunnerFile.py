

import os

import stripe
from flask import Flask, jsonify, request, render_template, url_for
# r = requests.get('https://httpbin.org/get')
# print(r.status_code)

app = Flask(__name__)


# using testing environment

# stripe_keys = {
#   'secret_key': 'pk_test_51IWH5AJ4M3Bt1b7TX2jpgKXki1TELYDyiz5VsNjP8RoTE5chfBaWfgOo9yNFCmeAU3wsXo63iGJaBSg1dg3Ox4At00Mk4jVtXU',
#   'publishable_key': 'pk_test_51IWH5AJ4M3Bt1b7TX2jpgKXki1TELYDyiz5VsNjP8RoTE5chfBaWfgOo9yNFCmeAU3wsXo63iGJaBSg1dg3Ox4At00Mk4jVtXU'
# }


app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51Ib4VfBvhmRsAY8LWdqkxz5jziPQ1YmxCjuFHuQCaJyMNjoJSipniNaC1lh9ZocTLnpaxVWwgKkFSeX76ACHNqZP007ogKEoHo",
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Ib4VfBvhmRsAY8L6GHK8qRa5rHMl8oF4Innv0nchtswuquNwU9xMQlTycj80UGIpPWkw7BxO23cTlKRCJlUc3ll00ntxbvemn'
# config is an object for flask
# The config is actually a subclass of a dictionary and can be modified just like any dictionary:


# stripe_keys = {
#   'secret_key': os.environ['STRIPE_SECRET_KEY'],
#   'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
# }

# use secret key in the app

stripe.api_key = app.config['STRIPE_SECRET_KEY']
print(
stripe.api_key)