from app.models.types import ProductType
from .templates import Product, Vendor
from scrapers.cannon_keys import CannonKeys

ck_products = [
    Product(
        url='switches',
        type=ProductType.switch,
        ignore=[],
        remove='\s*Switch\w*\s*\(?\d*\)?'
    ),
    # Product(
    #     url='keycaps', 
    #     type=ProductType.keyset,
    #     remove=r'( Keycaps| Keycap Set)'
    # ),
    # Product(
    #     url='keyboards',
    #     type=ProductType.kit
    # ),
    # Product(
    #     url='diy-kits',
    #     type=ProductType.pcb, 
    #     ignore=['elite-c', 'proton'],
    #     include=['pcb'],
    #     remove=' PCB'
    # ),
    # Product(
    #     url='diy-kits',
    #     type=ProductType.kit,
    #     include=['kit']
    # ),
    # Product(
    #     url='deskpads',
    #     type=ProductType.deskmat,
    #     remove=' Deskpad'
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
