from app.models.types import ProductType
from .templates import Product, Vendor
from scrapers.cannon_keys import CannonKeys

ck_products = [
    # Product(
    #     url='switches',
    #     type=ProductType.switch,
    #     ignore=[],
    #     remove='(Linear|Tactile|Clicky|Switch|\(\d*\))\s*'
    # ),
    # Product(
    #     url='keycaps', 
    #     type=ProductType.keyset,
    #     remove=r'( Keycaps| Keycap Set)'
    # ),
    # Product(
    #     url='frontpage',
    #     type=ProductType.kit
    # ),
    # Product(
    #     url='diy-kits',
    #     type=ProductType.pcb, 
    #     ignore=['elite-c', 'proton'],
    #     include=['pcb'],
    #     remove=' PCB'
    # ),
    Product(
        url='pcbs',
        type=ProductType.pcb,
        remove=' PCB'
    ),
    # Product(
    #     url='deskmats',
    #     type=ProductType.deskmat,
    #     remove=' Deskmat\w*|\[GB\] '
    # ),
    # Product(
    #     url='miscellaneous',
    #     type=ProductType.stabilizer,
    #     include=['stabilizers']
    # ),
    # Product(
    #     url='miscellaneous',
    #     type=ProductType.lube,
    #     include=['lubricants'],
    #     remove='Lubricants '
    # ),
    # Product(
    #     url='miscellaneous',
    #     type=ProductType.film,
    #     include=['films']
    # ),
    # Product(
    #     url='miscellaneous',
    #     type=ProductType.spring,
    #     include=['springs']
    # ),
    # Product(
    #     url='miscellaneous',
    #     type=ProductType.tool,
    #     include=['puller, opener']
# )
]

ck_vendor = Vendor(
    scraper=CannonKeys,
    name='Cannon Keys',
    url="https://cannonkeys.com/collections/",
    products=ck_products
)
