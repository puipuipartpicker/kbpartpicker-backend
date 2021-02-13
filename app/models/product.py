import re
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from ._base import BaseModel
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Boolean
from .types import (
    ProductType, KeyboardFormFactor,
    StabilizerSize, StabilizerType,
    SwitchType, SwitchProfile, KeyboardLayout
)

class Product(BaseModel):

    name = Column(String, nullable=False)
    img_url = Column(String)
    product_type = Column(pgEnum(ProductType, name='product_type'))
    stabilizer_size = Column(pgEnum(StabilizerSize, name='stabilizer_size'))
    keyboard_form_factor = Column(pgEnum(KeyboardFormFactor, name='keyboard_form_factor'))
    keyboard_layout = Column(pgEnum(KeyboardLayout, name='keyboard_layout'))
    stabilizer_type = Column(pgEnum(StabilizerType, name='stabilizer_type'))
    switch_type = Column(pgEnum(SwitchType, name='switch_type'))
    switch_profile = Column(pgEnum(SwitchProfile, name='switch_profile'))
    hotswap = Column(Boolean)
