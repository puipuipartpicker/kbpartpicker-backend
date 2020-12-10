from ._base import Base

from sqlalchemy.schema import Column
from sqlalchemy.types import Text

class Vendor(Base):

    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)