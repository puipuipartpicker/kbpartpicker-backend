# import time
import re
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 

from ._base import BaseScraper
from app.models.types import ProductType, LayoutType, SizeType, StabilizerType
# from app.models import Product, Vendor, VendorProductAssociation
# from utils.catch_noelem_exception import CatchNoElem
# from utils.regex_dict import RegexDict


class CannonKeys(BaseScraper):

    def __init__(self, session, driver, product, name, url):
        super(CannonKeys, self).__init__(session, driver, product, name, url)

    def _get_variants(self, name):
        variants = []
        options = self._get_options(1)
        if not options:
            return [self._get_details(name)]

        options_are_count = self._are_options_count()
        if not options_are_count:
            for o in options:
                o.click()
                variants.append(self._get_details(name, o.text))
            return variants
        else:
            options[0].click()  # only need the first option to calculate per item price
            return [self._get_details(name, options[0].text, count=options_are_count)]

        if self.product.type == ProductType.stabilizer:
            stabilizer_types = self._get_options(1)
            for o in options:
                o.click()
                if stabilizer_types:
                    for t in stabilizer_types:
                        t.click()
                        variants.append(self._get_details(name, o.text, t.text))
                else:
                    variants.append(self._get_details(name, o.text))
            return variants