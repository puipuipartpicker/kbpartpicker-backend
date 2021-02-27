import re
from models.types import ProductType, KeyboardFormFactor, StabilizerSize
from models import Product, Vendor, VendorProductAssociation


class DatabaseAction():

    def __init__(self, session):
        self.session = session

    def update_or_insert(self, product_details, pv_details):
        product, p_is_new = Product.get_or_create(
            self.session,
            name=product_details.get('name'),
            product_type=product_details.get('product_type')
        )
        pv, pv_is_new = VendorProductAssociation.get_or_create(
            self.session,
            product_id=product.id,
            vendor_id=pv_details.get('vendor_id')
        )
        product.populate(**product_details)
        pv.populate(**pv_details)
        self.session.commit()
        print(
            f"{'Inserted' if p_is_new else 'Updated'}"
            f" {product.name} for {pv.vendor.name}."
        )
