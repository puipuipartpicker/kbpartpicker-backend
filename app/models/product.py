import re
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from config.database import db
from ._base import BaseModel
from .types import (
    ProductType, KeyboardFormFactor,
    StabilizerSize, StabilizerType,
    SwitchType, SwitchProfile, KeyboardLayout
)

class Product(BaseModel):

    __tablename__ = 'products'

    name = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String())
    product_type = db.Column(pgEnum(ProductType, name='product_type'))
    stabilizer_size = db.Column(pgEnum(StabilizerSize, name='stabilizer_size'))
    keyboard_form_factor = db.Column(pgEnum(KeyboardFormFactor, name='keyboard_form_factor'))
    keyboard_layout = db.Column(pgEnum(KeyboardLayout, name='keyboard_layout'))
    stabilizer_type = db.Column(pgEnum(StabilizerType, name='stabilizer_type'))
    switch_type = db.Column(pgEnum(SwitchType, name='switch_type'))
    switch_profile = db.Column(pgEnum(SwitchProfile, name='switch_profile'))
    hotswap = db.Column(db.Boolean)
