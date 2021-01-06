from ._base import BaseModel
from config.database import db

class Country(BaseModel):

    __tablename__ = 'countries'

    country_name = db.Column(db.String(), nullable=False)
    country_code = db.Column(db.Integer, nullable=False)
    iso_code = db.Column(db.String(), nullable=False)
    currency_code = db.Column(db.String(), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)