from flask import Blueprint
from flask_cors import cross_origin, CORS
from models import Product
from models.types import ProductType
from api.handlers import search

categories = Blueprint('categories', __name__)
# CORS(categories, support_credentials=True, resources={r"/*": {"origins": "*"}})
CORS(categories, resources={r"/*"}, origins=["*"], support_credentials=True)

@categories.route('/switch/search')
# @cross_origin(supports_credentials=True)
def switch():
    product = Product.query.filter_by(product_type=ProductType.switch)
    return search(product)


@categories.route('/pcb/search')
# @cross_origin(supports_credentials=True)
def pcb():
    product = Product.query.filter_by(product_type=ProductType.pcb)
    return search(product)


@categories.route('/case/search')
# @cross_origin(supports_credentials=True)
def case():
    product = Product.query.filter_by(product_type=ProductType.case)
    return search(product)


@categories.route('/plate/search')
# @cross_origin(supports_credentials=True)
def plate():
    product = Product.query.filter_by(product_type=ProductType.plate)
    return search(product)


@categories.route('/stabilizer/search')
# @cross_origin(supports_credentials=True)
def stabilizer():
    product = Product.query.filter_by(product_type=ProductType.stabilizer)
    return search(product)


@categories.route('/keycaps/search')
# @cross_origin(supports_credentials=True)
def keycaps():
    product = Product.query.filter_by(product_type=ProductType.keyset)
    return search(product)
