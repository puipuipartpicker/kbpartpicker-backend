import os
from flask import Flask, request, jsonify

from api.exceptions import InvalidUsage, NotFound, InternalServerError
from app.models import Product, VendorProductAssociation
from app.models.types import ProductType


def get():
    if request.method == "GET":
        product_id = int(request.args.get("id"))
        product = Product.query.get(product_id)
        if not product:
            raise NotFound(f"Product not found for id: {product_id}")
        pvs = VendorProductAssociation.query.filter(
            VendorProductAssociation.product_id == product_id
        )
        res = product.to_dict()
        res["vendors"] = [pv.to_dict() for pv in pvs]
        return jsonify(res)


def search():
    if request.method == "GET":
        category = request.args.get("category")
        query = request.args.get("query")
        search = f"%{query}%"
        products = Product.query.filter(
            Product.name.ilike(search),
            Product.product_type == ProductType[category]
        )
        pvs = VendorProductAssociation.query.filter(
            VendorProductAssociation.product_id.in_([p.id for p in products])
        )
        return jsonify([dict(
            id=pv.product.id,
            name=pv.product.name,
            img_url=pv.product.img_url,
            in_stock=pv.in_stock,
            price=pv.price,
            vendor=dict(name=pv.vendor.name, url=pv.vendor.url)
        ) for pv in pvs])
    
def index():
    return "<h1>KBPARTPICKER TOWN!!</h1>"
