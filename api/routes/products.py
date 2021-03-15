from flask import Blueprint
from api.handlers import get, get_product

products = Blueprint('products', __name__)

products.add_url_rule('/<int_list:product_ids>', 'get', get)
products.add_url_rule('/get_product', 'get_product', get_product)
