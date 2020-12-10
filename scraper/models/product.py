import re
from ._base import Base

from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Text, Integer, Float
from sqlalchemy_utils import ChoiceType
from sqlalchemy.event import listen

from .types.product_type import ProductType
from .types.layout_type import LayoutType
from .types.size_type import SizeType

class Product(Base):

    name = Column(Text, nullable=False)
    img_url = Column(Text, nullable=False)
    type = Column(ChoiceType(ProductType, impl=Integer()), nullable=False)
    size = Column(ChoiceType(SizeType, impl=Integer()))
    layout = Column(ChoiceType(LayoutType, impl=Integer()))
    hotswap = Column(Boolean)

    def cleanup_name(self):
        if self.type == ProductType.switch:
            self.name = re.sub(r' Switches', '', self.name)


def cleanup_name(mapper, connection, target):
    target.cleanup_name()


listen(Product, 'before_insert', cleanup_name)
