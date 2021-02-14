from flask import jsonify


def handle_http_error(exception):
    if hasattr(exception, 'payload'):
        rv = dict(exception.payload or ())
    else:
        rv = dict()
    rv['message'] = str(exception)
    response = jsonify(rv)
    response.status_code = exception.code
    return response


def handle_app_error(exception):
    rv = dict()
    rv['message'] = str(exception)
    response = jsonify(rv)
    response.status_code = 500
    return response
