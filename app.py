from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper.models import Product, VendorProductAssociation
from scraper.models.types import ProductType

app = FlaskAPI(__name__)
CORS(app)

engine = create_engine('postgres+psycopg2://vi:password@localhost:5432/kbpartpicker')
session = sessionmaker(bind=engine)()

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        print(request.json)
        return jsonify("Sent")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        print(request.json)
        category = request.data["category"]
        query = request.data["query"]
        search = "%{}%".format(query)
        products = session.query(Product).filter(
            Product.name.like(search),
            Product.type == ProductType[category]
        )
        pvs = session.query(VendorProductAssociation).filter_by(
            VendorProductAssociation.product_id.in_([p.id for p in products])
        )
        return [dict(
            name=pv.product.name,
            img_url=pv.product.img_url,
            in_stock=pv.in_stock,
            price=pv.price,
            vendor=pv.vendor.name
        ) for pv in pvs]

if __name__ == "__main__":
    app.run(debug=True)