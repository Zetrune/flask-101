# pylint: disable=missing-docstring
from copy import deepcopy
from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)

INITIAL_PRODUCTS = [
    {"id": 1, "name": "Skello"},
    {"id": 2, "name": "Socialive.tv"},
    {"id": 3, "name": "lemonde.fr"}
]

PRODUCTS = deepcopy(INITIAL_PRODUCTS)

@app.route('/')
def hello():
    return "Hello World!"

@app.route("/api/v1/products")
def get_product_list():
    return jsonify(PRODUCTS)

def init_product_list():
    global PRODUCTS
    PRODUCTS = deepcopy(INITIAL_PRODUCTS)

def product_exist(product_id):
    if product_id == 0 or product_id > len(PRODUCTS):
        app.logger.error(f"product ID [{product_id}] does not exist in PRODUCTS - Incorrect index")
        return False
    product = PRODUCTS[product_id - 1]
    app.logger.info(product)
    if product["name"] is None:
        app.logger.error(f"product ID [{product_id}] does not exist in PRODUCTS - None value")
        return False
    return True

def erase_product(product_id):
    product_index = product_id - 1
    product = PRODUCTS[product_index]
    name = product["name"]
    app.logger.info(f"Erase product ID [{product_id}] of value [{name}]")
    product["name"] = None
    PRODUCTS[product_index] = product
    return product

def retrieve_product(product_id):
    product_index = product_id - 1
    product = PRODUCTS[product_index]
    name = product["name"]
    app.logger.info(f"Retrieve product ID [{product_id}] of value [{name}]")
    return product

@app.route("/api/v1/products/<int:product_id>", methods=['GET'])
def get_product(product_id):
    if not product_exist(product_id):
        app.logger.error(f"Unable to GET product ID [{product_id}]")
        abort(404)
    product = retrieve_product(product_id)
    app.logger.info(f"product ID [{product_id}] exist in PRODUCTS")
    return make_response(jsonify(product), 200)

@app.route("/api/v1/products/<int:product_id>", methods=['DELETE'])
def delete_product(product_id):
    if not product_exist(product_id):
        app.logger.error(f"Unable to DELETE product ID [{product_id}]")
        abort(404)
    erase_product(product_id)
    app.logger.info(f"product ID [{product_id}] has been deleted from PRODUCTS")
    return make_response("", 204)

def get_empty_id():
    nb_product = len(PRODUCTS)
    new_id = nb_product + 1
    for i in range(nb_product):
        if not product_exist(i + 1):
            new_id = i + 1
        break
    return new_id

@app.route("/api/v1/products", methods=['POST'])
def create_product():
    body = request.get_json()
    if not "name" in body or body["name"] is None:
        abort(422)
    target_name = body["name"]
    target_id = get_empty_id()
    new_product = {"id": target_id, "name": target_name}
    PRODUCTS.insert(target_id - 1, new_product)
    app.logger.info(f"product ID [{target_id}] has been created with value [{target_name}]")
    return make_response(jsonify(target_id), 201)
