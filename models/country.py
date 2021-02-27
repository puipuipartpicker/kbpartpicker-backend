from ._base import BaseModel
from sqlalchemy.schema import Column
from sqlalchemy.types import Float, String

class Country(BaseModel):

    country_name = Column(String(), nullable=False)
    country_code = Column(String())
    iso_code = Column(String())
    currency_code = Column(String())
    exchange_rate = Column(Float, nullable=False)
