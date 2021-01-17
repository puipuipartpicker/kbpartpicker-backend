import logging
from selenium.common.exceptions import NoSuchElementException

from functools import wraps


def CatchNoElem(return_none=True):
    def _decorator(func):
        @wraps(func)
        def _internal(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NoSuchElementException:
                if not return_none:
                    raise Exception("Can't get element for a required field")
                return None, None
        return _internal
    return _decorator
