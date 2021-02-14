import os
from flask import request, jsonify

from api.exceptions import *
from app.models import Product, VendorProductAssociation
from app.models.types import ProductType


def get(product_id):
    if request.method != "GET":
        raise MethodNotAllowed(request.method)
    product = Product.query.get(product_id)
    if not product:
        raise NotFound(Product, product_id)
    pvs = VendorProductAssociation.query.filter(
        VendorProductAssociation.product_id == product_id
    )
    if not pvs:
        raise NotFound(VendorProductAssociation, product_id)
    res = product.to_dict()
    res["vendors"] = [pv.to_dict(name=pv.vendor.name) for pv in pvs]
    return jsonify(res)
