# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

import os
from flask import Flask, request, jsonify
# from flask_api import FlaskAPI
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Product, VendorProductAssociation
from models.types import ProductType

app = Flask(__name__)
CORS(app)

prd = os.environ.get('DATABASE_URL')

if prd:
    print('prd')
    engine = create_engine(prd)
    session = sessionmaker(bind=engine)()
else:
    engine = create_engine('postgres+psycopg2://vi:password@localhost:5432/kbpartpicker')
    session = sessionmaker(bind=engine)()

# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         print(request.json)
#         return jsonify("Sent")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        print(request.json)
        category = request.json["category"]
        query = request.json["query"]
        print(category)
        search = "%{}%".format(query)
        products = session.query(Product).filter(
            Product.name.like(search),
            Product.type == ProductType[category]
        )
        print(products.all())
        pvs = session.query(VendorProductAssociation).filter(
            VendorProductAssociation.product_id.in_([p.id for p in products])
        )
        print(pvs.all())
        return jsonify({"data": [dict(
            name=pv.product.name,
            img_url=pv.product.img_url,
            in_stock=pv.in_stock,
            price=pv.price,
            vendor=pv.vendor.name
        ) for pv in pvs]})
    
    @app.route('/')
    def index():
        return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(threaded=True, port=5000)