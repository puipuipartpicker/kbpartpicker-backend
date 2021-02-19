from flask import Blueprint
from flask_cors import cross_origin, CORS
from api.handlers import get

products = Blueprint('products', __name__)
# CORS(products, support_credentials=True, resources={r"/*": {"origins": "*"}})
CORS(products, resources={r"/*"}, origins=["*"], support_credentials=True)

products.add_url_rule('/<product_id>', 'get', get)
