from flask import Blueprint
from api.handlers import search

categories = Blueprint('categories', __name__)

categories.add_url_rule('/<product_type>/search', 'search', search)
