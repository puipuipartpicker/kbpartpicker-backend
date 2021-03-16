import re
import logging
from flask import request, jsonify
from vendors import nk_vendor, ck_vendor
from models import Product

logger = logging.getLogger('gunicorn.error')

def get_product():
    vendor_url = request.data.get("vendor_url")
    product_name = request.data.get("product_name")

    logger.info(vendor_url)
    logger.info(product_name)

    all_vendors = [nk_vendor, ck_vendor]
    vendor = [v for v in all_vendors if v.config.url in vendor_url][0]
    logger.info(vendor)
    if product_config := [
        p for p in vendor.config.products
        if f"{vendor.config.url}{p.url}" in vendor_url
    ]:
        product_name = re.sub(product_config[0].remove, '', product_name)
        logger.info(product_name)

    response = {"status": ""}
    if product_config and product_name in product_config[0].ignore:
        logger.info("Not Supported product")
        response["status"] = "Not Supported"
    elif product := Product.query.filter(Product.name.ilike(f"%{product_name}")).one():
        logger.info("Found product")
        logger.info(product.to_dict())
        response["status"] = "Found"
        response["found_record"] = product.to_dict()
    else:
        logger.info("Product Not Found")
        response["status"] = "Not Found"

    logger.info(response)
    return jsonify(response)
