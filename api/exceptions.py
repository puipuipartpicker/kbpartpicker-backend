from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppException(HTTPException):

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.code = status_code
        self.payload = payload

    def __str__(self):
        return self.message


class InvalidUsage(AppException):

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, 400, payload)


class NotFound(AppException):

    def __init__(self, target_class, target_id, status_code=None, payload=None):
        message = self._make_message(target_class, target_id)
        super().__init__(message, 404, payload)
    
    def _make_message(self, target_class, target_id):
        target = target_class.__name__
        if target == "VendorProductAssociation":
            return f"Couldn't find any vendors associated with product_id: {target_id}"
        return f"{target} not found for id: {target_id}"


class InternalServerError(AppException):

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message, 500, payload)


class MethodNotAllowed(AppException):

    def __init__(self, method, status_code=None, payload=None):
        message = self._make_message(method)
        super().__init__(message, 405, payload)

    def _make_message(self, method):
        return f"{method} not allowed for this URL!"
