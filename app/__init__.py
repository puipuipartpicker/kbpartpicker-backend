import os
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config.database import init_db, session


# TODO Add authorization
# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py


def create_app():
    app = FlaskAPI(__name__)
    # Configurations
    app.config.from_object('setup')
    CORS(app)
    admin = Admin(app, name='kbpartpicker', template_mode='bootstrap3')
    from .models import Product, Vendor, Country, VendorProductAssociation
    init_db()
    admin.add_view(ModelView(Product, session))
    admin.add_view(ModelView(Vendor, session))
    admin.add_view(ModelView(Country, session))
    return app

app = create_app()

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()
    session.remove()
    