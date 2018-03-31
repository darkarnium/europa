''' v1 of the Europa project API. '''

from flask import Blueprint

# Register a new blueprint for this API version.
router = Blueprint(__name__, __name__)

from europa.api.v1 import decorators
from europa.api.v1 import exceptions
from europa.api.v1 import endpoints
