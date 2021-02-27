import os
import logging
import sys
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config.database import init_db, session


# TODO Add authorization
# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py


def create_app():
    print('create flask app')
    app = FlaskAPI(__name__)
    # Configurations
    app.config.from_object('setup')
    # CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})
    CORS(app, resources={r"/*"}, origins=["*"], support_credentials=True)
    admin = Admin(app, name='kbpartpicker', template_mode='bootstrap3')
    from models import Product, Vendor, Country, VendorProductAssociation
    init_db()
    admin.add_view(ModelView(Product, session))
    admin.add_view(ModelView(Vendor, session))
    admin.add_view(ModelView(Country, session))
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)

    # Configure logging.
    app.logger.setLevel(logging.DEBUG)
    del app.logger.handlers[:]

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.formatter = logging.Formatter(
        fmt=u"%(asctime)s level=%(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    app.logger.addHandler(handler)
    return app

app = create_app()

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()
    session.remove()
