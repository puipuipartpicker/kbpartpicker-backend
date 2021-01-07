from app.models.types import ProductType
from .templates import Product, Vendor
from scrapers.novel_keys import NovelKeys

nk_products = [
    Product(
        url='switches',
        type=ProductType.switch,
        ignore=['Sample', 'Big'],
    ),
    Product(
        url='keycaps', 
        type=ProductType.keyset
    ),
    Product(
        url='keyboards',
        type=ProductType.kit
    ),
    Product(
        url='diy-kits',
        type=ProductType.pcb, 
        include=['pcb']
    ),
    Product(
        url='diy-kits',
        type=ProductType.kit,
        include=['kit']
    ),
    Product(
        url='miscellaneous',
        type=ProductType.stabilizer,
        include=['stabilizers']
    ),
    Product(
        url='miscellaneous',
        type=ProductType.lube,
        include=['lubricants']
    ),
    Product(
        url='miscellaneous',
        type=ProductType.film,
        include=['films']
    ),
    Product(
        url='miscellaneous',
        type=ProductType.spring,
        include=['springs']
    ),
    Product(
        url='miscellaneous',
        type=ProductType.tool,
        include=['puller, opener']
    )
]

nk_vendor = Vendor(
    scraper=NovelKeys,
    name='NovelKeys',
    url="https://novelkeys.xyz/collections/",
    products=nk_products
)
