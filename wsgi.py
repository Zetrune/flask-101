# pylint: disable=missing-docstring

from flask import Flask, jsonify, make_response
app = Flask(__name__)

PRODUCTS = [
    {'id': 1, 'name': 'Skello'},
    {'id': 2, 'name': 'Socialive.tv'},
    {'id': 3, 'name': 'lemonde.fr'}
]

@app.route("/api/v1/products")
def get_product_list():
    return jsonify(PRODUCTS)

@app.route("/api/v1/products/<int:id>")
def get_product(product_id):
    if product_id in PRODUCTS:
        product = PRODUCTS[product_id]
        status = 200
    else:
        product = {}
        status = 404
    response = make_response(jsonify(product), status)
    return response

@app.route('/')
def hello():
    return "Hello World!"
