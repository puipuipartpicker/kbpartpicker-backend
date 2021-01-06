from ._base import BaseModel
from config.database import db

class Vendor(BaseModel):

    __tablename__ = 'vendors'

    name = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    country = db.relationship(
        'Country', lazy='select',
        backref=db.backref('countries', lazy='joined'))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))