import logging
from selenium.common.exceptions import NoSuchElementException

from functools import wraps


def CatchNoElem(return_value=None):
    def _decorator(func):
        @wraps(func)
        def _internal(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NoSuchElementException:
                return None
        return _internal
    return _decorator