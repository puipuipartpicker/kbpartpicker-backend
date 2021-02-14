from flask import Blueprint
from api.handlers import get

products = Blueprint('products', __name__)

products.add_url_rule('/<product_id>', 'get', get)
