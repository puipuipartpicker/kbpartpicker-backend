from flask import Blueprint
from app.models import Product
from app.models.types import ProductType
from api.handlers import search

categories = Blueprint('categories', __name__)

@categories.route('/switch/search')
def switch():
    product = Product.query.filter_by(product_type=ProductType.switch)
    return search(product)


@categories.route('/pcb/search')
def pcb():
    product = Product.query.filter_by(product_type=ProductType.pcb)
    return search(product)


@categories.route('/case/search')
def case():
    product = Product.query.filter_by(product_type=ProductType.case)
    return search(product)


@categories.route('/plate/search')
def plate():
    product = Product.query.filter_by(product_type=ProductType.plate)
    return search(product)


@categories.route('/stabilizer/search')
def stabilizer():
    product = Product.query.filter_by(product_type=ProductType.stabilizer)
    return search(product)


@categories.route('/keycaps/search')
def keycaps():
    product = Product.query.filter_by(product_type=ProductType.keyset)
    return search(product)
