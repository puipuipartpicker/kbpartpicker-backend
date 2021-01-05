from attr import attrs, attrib
from attr.validators import instance_of

from utils.list_of import list_of
from . import Product


@attrs
class Vendor:
    scraper = attrib()
    name = attrib(validator=instance_of(str))
    url = attrib(validator=instance_of(str))
    products = attrib(validator=list_of(Product))
