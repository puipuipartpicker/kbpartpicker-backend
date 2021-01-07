from ._base import BaseModel
from config.database import db

class VendorProductAssociation(BaseModel):

    __tablename__ = 'vendor_product_associations'

    product = db.relationship(
        'Product', lazy='select',
        backref=db.backref('vendor_product_associations'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    vendor = db.relationship(
        'Vendor', lazy='select',
        backref=db.backref('vendor_product_associations'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    price = db.Column(db.Float)
    in_stock = db.Column(db.Boolean)
    url = db.Column(db.Text)

    # def update_or_insert(self, session, vendor):
        