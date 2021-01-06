import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from config.database import db


def create_app():
    app = Flask(__name__)
    # Configurations
    app.config.from_object('setup')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    CORS(app)
    admin = Admin(app, name='kbpartpicker', template_mode='bootstrap3')
    from .models import Product, Vendor, Country, VendorProductAssociation
    db.init_app(app)
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Vendor, db.session))
    # db.create_all()
    Migrate(app, db)
    return app

app = create_app()


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
# app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()