from ._base import BaseModel
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer

class Vendor(BaseModel):

    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    country = relationship(
        'Country', lazy='select',
        backref=backref('countries', lazy='joined'))
    country_id = Column(Integer, ForeignKey('countries.id'))
