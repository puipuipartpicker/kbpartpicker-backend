import re
import logging
from flask import request, jsonify
from vendors import nk_vendor, ck_vendor
from models import Product, VendorProductAssociation

logger = logging.getLogger('gunicorn.error')

def get_product():
    vendor_url = request.data.get("vendor_url")
    product_url = request.data.get("product_url")
    pv_url = _merge_url(vendor_url, product_url)

    response = {"status": ""}
    pv = VendorProductAssociation.query.filter(
        VendorProductAssociation.url.ilike(f"%{pv_url}")
    ).first()
    if not pv:
        response["status"] = "Not Found"
    else:
        response["status"] = "Found"
        response["found_record"] = pv.product.to_dict()

    logger.info(response)
    return jsonify(response)


def _merge_url(s1, s2):
    i = 0
    while not s2.startswith(s1[i:]):
        i += 1
    return s1[:i] + s2
