import os
from flask import request, jsonify

from api.exceptions import *
from models import Product, VendorProductAssociation
from models.types import ProductType


def search(product_type):
    product = Product.query.filter_by(product_type=ProductType[product_type])
    if request.method != "GET":
        raise MethodNotAllowed(request.method)
    query = request.args.get("query")
    if not query:
        raise Exception
    search = f"%{query}%"
    products = product.filter(
        Product.name.ilike(search)
    )
    if not products:
        raise Exception
    pvs = VendorProductAssociation.query.filter(
        VendorProductAssociation.product_id.in_([p.id for p in products])
    )
    if not pvs:
        raise Exception
    return jsonify([dict(
        id=pv.product.id,
        name=pv.product.name,
        img_url=pv.product.img_url,
        in_stock=pv.in_stock,
        price=pv.price,
        vendor=dict(name=pv.vendor.name, url=pv.vendor.url)
    ) for pv in pvs])
