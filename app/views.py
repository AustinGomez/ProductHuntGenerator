from flask import render_template, jsonify
from flask_cors import CORS

from app import app, db
from app.models.models import Product

CORS(app)

@app.route('/api/products')
def Products(name=None):
    products = []
    print("querying")
    for product in db.session.query(Product):
        print("product")
        products.append(product)

    return jsonify(products=[product.serialize() for product in products])




