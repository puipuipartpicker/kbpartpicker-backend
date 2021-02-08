# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
from app import app
from api.routes import get, search, index
from api.exception_handlers import handle_exception

errors_to_handle = [400, 404, 500]
for error in errors_to_handle:
    app.register_error_handler(error, handle_exception)

app.add_url_rule('/', 'index', index)
app.add_url_rule('/get', 'get', get)
app.add_url_rule('/search', 'search', search)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(threaded=True, port=5000)
