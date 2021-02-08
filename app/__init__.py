import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from config.database import db


# TODO Add authorization
# https://github.com/flask-admin/flask-admin/blob/master/examples/auth-flask-login/app.py


def create_app():
    app = Flask(__name__)
    # Configurations
    app.config.from_object('setup')
    CORS(app)
    admin = Admin(app, name='kbpartpicker', template_mode='bootstrap3')
    from .models import Product, Vendor, Country, VendorProductAssociation
    db.init_app(app)
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Vendor, db.session))
    admin.add_view(ModelView(Country, db.session))
    # db.create_all()
    Migrate(app, db)
    return app

app = create_app()
