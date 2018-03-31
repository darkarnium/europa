''' Defines decorators for use throughout V1 of The Europa project API. '''

from functools import wraps

from flask import g
from flask import request

from europa.api.v1 import exceptions    


def validated(fields=None, optional=False):
    '''
    Validate the request contains a valid JSON document, and that all required
    fields are present. If not, raise an exception and kill request processing.
    '''
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            document = request.get_json()
            if document is None:
                raise exceptions.InvalidClientRequest('No JSON provided')

            # If 'Optional' check, allow any fields as long as they appear in
            # the fields list, rather than ensuring they ALL exist.
            if optional:
                # Ensure present fields are allowed.
                for field in document:
                    if field not in fields:
                        raise exceptions.InvalidClientRequest(
                            "'{}' field not permitted".format(field)
                        )
            else:
                # Ensure required fields are present in the request.
                for field in fields:
                    if document.get(field) is None:
                        raise exceptions.InvalidClientRequest(
                            "'{}' field missing".format(field)
                        )
            return func(*args, **kwargs)

        # Decorators with arguments must return a function to be invoked.
        return decorated_function
    return decorator
