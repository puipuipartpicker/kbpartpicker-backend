import re
from app.models.types import ProductType, LayoutType, SizeType
from app.models import Product, Vendor, VendorProductAssociation


class DatabaseAction():

    def __init__(self, session, product, vendor):
        self.session = session
        self.product = product
        self.vendor = vendor

    def update_or_insert(self, name, img_url, price, in_stock, pv_url):
        product, p_is_new = Product.get_or_create(
            self.session,
            name=name,
            product_type=self.product.type
        )
        pv, pv_is_new = VendorProductAssociation.get_or_create(
            self.session,
            product_id=product.id,
            vendor_id=self.vendor.id
        )
        product.img_url = img_url
        pv.price = price
        pv.in_stock = in_stock
        pv.url = pv_url
        self.session.commit()
        print(product.name, pv.vendor.name, "insert" if p_is_new else "update")
