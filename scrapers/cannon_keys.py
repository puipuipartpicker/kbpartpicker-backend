# import time
import re
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 

from ._base import BaseScraper
from app.models.types import (
    ProductType,
    KeyboardFormFactor,
    StabilizerSize,
    StabilizerType,
    SwitchType
)
# from app.models import Product, Vendor, VendorProductAssociation
# from utils.catch_noelem_exception import CatchNoElem
# from utils.regex_dict import RegexDict


class CannonKeys(BaseScraper):

    def __init__(self, session, driver, product, name, url):
        super(CannonKeys, self).__init__(session, driver, product, name, url)

    def _get_variant_fields(self, name):
        variants = []
        drop_downs = self._get_options_and_type()
        if not drop_downs:
            if self.product.type == ProductType.switch:
                return [{'name': name, 'count_option': self._get_count(name)}]
            return [{'name': name}]

        count_options = drop_downs.get("Quantity")
        type_options = (
            drop_downs.get("Type") or
            drop_downs.get("Deskmat") or
            drop_downs.get("Variant") or
            drop_downs.get("Kit") or
            drop_downs.get("Color") or
            drop_downs.get("Weight") or
            (drop_downs.get("Style") if self.product.type != ProductType.stabilizer else None)
        )
        size_options = drop_downs.get("Size")
        stab_type_options = drop_downs.get("Style")

        if count_options and not type_options:
            count_options[0].click()  # only need the first option to calculate per item price
            return [{'name': name, 'count_option': count_options[0].text}]
        elif type_options:
            for t in type_options:
                t.click()
                if count_options:
                    count_options[0].click()
                    variants.append({'name': name, 'type_option': t.text, 'count_option': count_options[0].text})
                else:
                    variants.append({'name': name, 'type_option': t.text})
            return variants
        elif size_options:
            for si in size_options:
                si.click()
                if stab_type_options:
                    for st in stab_type_options:
                        st.click()
                        variants.append({'name': name, 'stab_size': si.text, 'stab_type': st.text})
                else:
                    variants.append({'name': name, 'stab_size': si.text})
            return variants
    
    def _get_count(self, name):
        # TODO: Refactor
        count = re.search(r'\((\d+)\)', name)
        if count:
            return count.group(1)
        try:
            p = self.driver.find_element_by_xpath('//p[@data-mce-fragment="1"]')
        except NoSuchElementException:
            return None
        return re.search(r'[=:-]\s*(\d+)', p.text, re.I).group(1)

    def _get_switch_type(self, variant):
        if self.product.type != ProductType.switch:
            return None

        switch_types = [s.name for s in SwitchType]
        description = self.driver.find_element_by_class_name("product-single__description").text.lower()
        switch_type = list(filter(lambda t: t in description, switch_types))
        if switch_type:
            return SwitchType[switch_type.pop()]

    def _get_stabilizer_type(self, type_name):
        pass
