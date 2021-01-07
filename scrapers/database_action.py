import re
from app.models.types import ProductType, LayoutType, SizeType
from app.models import Product, Vendor, VendorProductAssociation


class DatabaseAction():

    def __init__(self, session, product, vendor):
        self.session = session
        self.product = product
        self.vendor = vendor

    def update_or_insert(self, product_details, pv_details):
        product, p_is_new = Product.get_or_create(
            self.session,
            name=product_details.get('name'),
            product_type=self.product.type
        )
        pv, pv_is_new = VendorProductAssociation.get_or_create(
            self.session,
            product_id=product.id,
            vendor_id=self.vendor.id
        )
        # TODO: anyway to do these lines programmatically?
        product.img_url = product_details.get('img_url')
        product.size = product_details.get('size')
        product.layout = product_details.get('layout')
        product.stabilizer_type = product_details.get('stabilizer_type')
        product.hotswap = product_details.get('hotswap')
        pv.price = pv_details.get('price')
        pv.in_stock = pv_details.get('in_stock')
        pv.url = pv_details.get('pv_url')
        self.session.commit()
        print(product.name, pv.vendor.name, "insert" if p_is_new else "update")
