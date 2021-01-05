from models.types import ProductType
from .templates import Product, Vendor
from scrapers.novel_keys import NovelKeys

nk_products = [
    Product(
        url='switches',
        type=ProductType.switch,
        ignore=['Sample', 'Big']
    ),
    Product(
        url='keycaps', 
        type=ProductType.keyset
    )
]

nk_vendor = Vendor(
    scraper=NovelKeys,
    name='NovelKeys',
    url="https://novelkeys.xyz/collections/",
    products=nk_products
)
