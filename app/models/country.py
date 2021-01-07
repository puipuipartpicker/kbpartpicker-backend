from ._base import BaseModel
from config.database import db

class Country(BaseModel):

    __tablename__ = 'countries'

    country_name = db.Column(db.String(), nullable=False)
    country_code = db.Column(db.String())
    iso_code = db.Column(db.String())
    currency_code = db.Column(db.String())
    exchange_rate = db.Column(db.Float, nullable=False)