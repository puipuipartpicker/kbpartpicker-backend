from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppException(Exception):

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidUsage(AppException):
    status_code = 400


class NotFound(AppException):
    status_code = 404


class InternalServerError(AppException):
    status_code = 500
