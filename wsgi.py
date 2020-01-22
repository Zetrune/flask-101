# pylint: disable=missing-docstring
from flask import Flask, jsonify, make_response
import sys

app = Flask(__name__)

PRODUCTS = [
    {'id': 1, 'name': 'Skello'},
    {'id': 2, 'name': 'Socialive.tv'},
    {'id': 3, 'name': 'lemonde.fr'}
]

@app.route("/api/v1/products")
def get_product_list():
    return jsonify(PRODUCTS)

@app.route("/api/v1/products/<int:product_id>")
def get_product(product_id):
    if product_id == 0 or product_id > len(PRODUCTS):
        app.logger.info(f"product ID [{product_id}] does not exist in PRODUCTS")
        product = None
        status = 404
    else:
        product_index = product_id - 1
        product = PRODUCTS[product_index]
        app.logger.info(f"product ID [{product_id}] exist in PRODUCTS")
        status = 200
    response = make_response(jsonify(product), status)
    return response

@app.route('/')
def hello():
    return "Hello World!"
