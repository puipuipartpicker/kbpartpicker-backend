from app.models.types import ProductType
from .templates import Product, Vendor, Config
from scrapers.cannon_keys import CannonKeys

ck_products = [
    Product(
        url='switches',
        type=ProductType.switch,
        ignore=[],
        remove='(Linear|Tactile|Clicky|Switch|\(\d*\))\s*'
    ),
    Product(
        url='frontpage',
        type=ProductType.kit
    ),
    Product(
        url='pcbs',
        type=ProductType.pcb,
        remove=' PCB'
    ),
    Product(
        url='deskmats',
        type=ProductType.deskmat,
        remove=' Deskmat\w*|\[GB\] '
    ),
    # Product(
    #     url='accessories',
    #     type=ProductType.stabilizer,
    #     include=['stabilizers']
    # ),
    Product(
        url='accessories',
        type=ProductType.lube,
        include=['lubricants'],
        remove='Lubricants '
    ),
    # Product(
    #     url='accessories',
    #     type=ProductType.film,
    #     include=['films']
    # ),
    # Product(
    #     url='accessories',
    #     type=ProductType.spring,
    #     include=['springs']
    # ),
    # Product(
    #     url='accessories',
    #     type=ProductType.tool,
    #     include=['puller, opener']
# )
]

ck_vendor = Vendor(
    scraper=CannonKeys,
    config=Config(
        name='Cannon Keys',
        url="https://cannonkeys.com/collections/",
        products=ck_products
    )
)
