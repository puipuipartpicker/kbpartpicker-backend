from attr import attrs, attrib
from attr.validators import instance_of, optional

from utils.list_of import list_of
from models.types import ProductType


@attrs
class Product:
    url = attrib(validator=instance_of(str))
    type = attrib(validator=instance_of(ProductType))
    ignore = attrib(validator=optional(list_of(str)), default=[])
    include = attrib(validator=optional(list_of(str)), default=[])
