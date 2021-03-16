import re
from flask import request, jsonify
from vendors import nk_vendor, ck_vendor
from models import Product

def get_product():
    vendor_url = request.data.get("vendor_url")
    product_name = request.data.get("product_name")

    all_vendors = [nk_vendor, ck_vendor]
    vendor = [v for v in all_vendors if v.config.url in vendor_url][0]
    if product_config := [
        p for p in vendor.config.products
        if f"{vendor.config.url}{p.url}" in vendor_url
    ]:
        product_name = re.sub(product_config[0].remove, '', product_name)

    response = {"status": ""}
    if product_config and product_name in product_config[0].ignore:
        response["status"] = "Not Supported"
    elif product := Product.query.filter(Product.name.ilike(f"%{product_name}")).one():
        response["status"] = "Found"
        response["found_record"] = product.to_dict()
    else:
        response["status"] = "Not Found"

    return jsonify(response)
