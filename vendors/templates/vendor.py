from attr import attrs, attrib
from attr.validators import instance_of

from utils.list_of import list_of
from . import Config


@attrs
class Vendor:
    scraper = attrib()
    config = attrib(validator=instance_of(Config))
