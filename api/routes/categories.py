from flask import Blueprint
from flask_cors import cross_origin, CORS
from models import Product
from models.types import ProductType
from api.handlers import search, get_product

categories = Blueprint('categories', __name__)

categories.add_url_rule('/<product_type>/search', 'search', search)
categories.add_url_rule('/<product_type>/get_product', 'get_product', get_product)
