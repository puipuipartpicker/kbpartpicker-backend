from ._base import BaseModel
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Boolean, Integer, Text, Float

class VendorProductAssociation(BaseModel):

    product = relationship(
        'Product', lazy='select',
        backref=backref('vendor_product_associations'))
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    vendor = relationship(
        'Vendor', lazy='select',
        backref=backref('vendor_product_associations'))
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    price = Column(Float)
    in_stock = Column(Boolean)
    url = Column(Text)
