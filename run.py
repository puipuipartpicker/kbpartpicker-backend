from app import app
from api.routes import categories, products
from api.exception_handlers import *
from werkzeug.exceptions import HTTPException
from api.exceptions import AppException, InternalServerError, InvalidUsage, NotFound
from utils.converters import IntListConverter


app.url_map.converters['int_list'] = IntListConverter

app.register_error_handler(HTTPException, handle_http_error)
app.register_error_handler(Exception, handle_app_error)

app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(products, url_prefix='/products')


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, threaded=True, port=5000)
