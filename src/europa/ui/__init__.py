''' The Europa project UI. '''

from flask import Blueprint
from flask import render_template

# Register a new blueprint for the UI router.
router = Blueprint(
    __name__,
    __name__,
    template_folder='templates',
    static_folder='static'
)


@router.route('/')
def retrieve_index():
    ''' Serves up the index page. '''
    return render_template('index.html')
