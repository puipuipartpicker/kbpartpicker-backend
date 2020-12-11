import re
from models.types import ProductType, LayoutType, SizeType
from models import Product, Vendor, VendorProductAssociation


class BaseScraper():

    def __init__(self, session, product, vendor):
        self.session = session
        self.product = product
        self.vendor = vendor

    def update_or_insert(self, name, img_url, price, in_stock):
        name = self._cleanup_name(name)
        product, is_new = Product.get_or_create(
            self.session,
            name=name,
            type=self.product.type
        )
        pv, is_new = VendorProductAssociation.get_or_create(
            self.session,
            product_id=product.id,
            vendor_id=self.vendor.id
        )
        product.img_url = img_url
        pv.price = price
        pv.in_stock = in_stock
        self.session.commit()

    def _cleanup_name(self, name):
        if self.product.type == ProductType.switch:
            name = re.sub(r' Switches', '', name)
        return name
