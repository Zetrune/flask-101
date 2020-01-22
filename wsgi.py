from flask import Flask, jsonify
app = Flask(__name__)

PRODUCTS = [
    {'id': 1, 'name': 'Skello' },
    {'id': 2, 'name': 'Socialive.tv' }
]

@app.route("/api/v1/products")
def products():
    return jsonify(PRODUCTS)

@app.route('/')
def hello():
    return "Hello World!"
