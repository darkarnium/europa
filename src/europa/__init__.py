''' The Europa project. '''

from flask import Flask
from flask import url_for
from flask import redirect
from flask import jsonify
from flask import request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from europa import ui
from europa import api
from europa import models


def initialize_all(config_file=None):
    ''' Initialize the main Europa application. '''
    application = Flask(__name__)
    application.register_blueprint(ui.router, url_prefix='/ui')
    application.register_blueprint(api.v1.router, url_prefix='/api/v1')

    # Register a redirect to ensure all non-API requests hit the UI.
    @application.route('/')
    def retrieve_index():
        return redirect(url_for('europa.ui.retrieve_index'))

    # If no configuration file is specified, load the testing defaults. If it
    # is, attempt to load the configuration from that file.
    if config_file is None:
        application.config.update(
            DEBUG=True,
            TESTING=True,
            JSON_AS_ASCII=False,
            SQLALCHEMY_DATABASE_URI='sqlite://',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        application.config.from_pyfile(config_file)

    # Setup the database, and the migrations library.
    models.db.init_app(application)
    Migrate(application, models.db)

    return application
