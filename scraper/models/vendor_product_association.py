from ._base import Base

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Text, BigInteger, Float, Boolean

class VendorProductAssociation(Base):

    product_id = Column(BigInteger, ForeignKey('products.id'))
    product = relationship(
        'Product', backref='vendor_product_associations', foreign_keys=[product_id])
    vendor_id = Column(BigInteger, ForeignKey('vendors.id'))
    vendor = relationship(
        'Vendor', backref='vendor_product_associations', foreign_keys=[vendor_id])
    price = Column(Float)
    in_stock = Column(Boolean)

    # def update_or_insert(self, session, vendor):
        