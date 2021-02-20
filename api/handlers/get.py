import os
import logging
from flask import request, jsonify
from flask_cors import cross_origin

from api.exceptions import *
from app.models import Product, VendorProductAssociation
from app.models.types import ProductType


logger = logging.getLogger('gunicorn.error')

def get(product_ids):
    if request.method != "GET":
        raise MethodNotAllowed(request.method)
    if not product_ids:
        raise InvalidUsage(
            "Please provide a product_id in the request parameter."
        )
    products = Product.query.filter(
        Product.id.in_(product_ids)
    )
    results = []
    for product in products:
        pvs = VendorProductAssociation.query.filter(
            VendorProductAssociation.product_id == product.id
        )
        if not pvs:
            raise NotFound(VendorProductAssociation, product.id)
        result = product.to_dict()
        result["vendors"] = [pv.to_dict(name=pv.vendor.name) for pv in pvs]
        results.append(result)
    if not results:
        raise NotFound(Product, product_ids)
    if missing_product_ids := set(product_ids) - set([p.id for p in products]):
        results.append(
            {"message": f"Products not found for ids: {list(missing_product_ids)}"}
        )
    if len(results) == 1:
        return jsonify(results.pop())
    return jsonify(results)
