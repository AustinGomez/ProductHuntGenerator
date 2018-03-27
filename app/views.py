from flask import render_template, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

from app import app, db
from app.models.models import Product

CORS(app)
api = Api(app)


class Products(Resource):
    def get(self):
        products = []
        print("querying")
        for product in db.session.query(Product):
            products.append(product)

        return jsonify(products=[product.serialize() for product in products])


api.add_resource(Products, '/api/products')


if __name__ == '__main__':
    app.run(debug=True)




