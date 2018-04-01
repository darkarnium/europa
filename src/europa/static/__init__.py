''' The Europa project static pages. '''

from flask import Blueprint
from flask import render_template

# Register a new blueprint for the static router.
router = Blueprint(__name__, __name__)


@router.route('/')
def static_root():
    ''' Serves a static webroot. '''
    return render_template('index.html')
