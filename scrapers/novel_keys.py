# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
import lxml.html
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

from ._base import BaseScraper
from models.types import (
    ProductType, KeyboardFormFactor,
    StabilizerSize, StabilizerType,
    SwitchType
)
from models import Product, Vendor, VendorProductAssociation
from utils.catch_noelem_exception import CatchNoElem
from utils.regex_dict import RegexDict


"""
TODO:
1. Add migration scripts (https://realpython.com/customize-django-admin-python/)
2. Write tests
3. Add currency (Create form for backend API to fill out manually)
4. Scrape all products on Novelkeys
"""

class NovelKeys(BaseScraper):

    def __init__(self, session, driver, nk_config):
        super(NovelKeys, self).__init__(session, driver, nk_config)
    
    def _get_variant_fields(self, name):
        variants = []
        drop_downs = self._get_options_and_type()
        if not drop_downs:
            return [{'name': name}]

        count_options = drop_downs.get("Count")
        type_options = self._get_type_options(drop_downs)
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

    def _get_type_options(self, drop_downs):
        return (
            drop_downs.get("Type") or
            drop_downs.get("Kit") or
            drop_downs.get("Color") or
            drop_downs.get("Weight") or
            (drop_downs.get("Style") if self.product.type != ProductType.stabilizer else None)
        )

    def _get_hotswappability(self, option):
        if not self._hotswappable_product():
            return False
        if option and option.lower() == 'hotswap':
            return True
        else:
            # TODO: fix(stale element reference: element is not attached to the page document)
            #       use a retry() decorator?
            ps = self.driver.find_elements_by_tag_name("p")
            ps = [p.text for p in ps]
            return 'hotswap' in  " ".join(ps).split(" ")

    def _get_stabilizer_type(self, type_name):
        if not (self.product.type != ProductType.stabilizer and type_name):
            return None
        formatted = '_'.join(type_name.lower().split(' '))
        return StabilizerType[formatted]

    def _get_switch_type(self, variant):
        if self.product.type != ProductType.switch:
            return None

        root = lxml.html.fromstring(self.driver.page_source)

        switch_types = [s.name for s in SwitchType]
        tables = root.xpath('.//table')
        if tables:
            return self._get_switch_type_from_table(variant, tables, switch_types)
        
        div = self.driver.find_element_by_class_name("product-single__description")
        lis = div.find_elements_by_tag_name("li")
        if lis:
            return self._get_switch_type_from_list(variant, lis, switch_types)

    def _get_switch_type_from_table(self, variant, tables, switch_types):
        buttons = self.driver.find_elements_by_class_name("accordion")
        index = 0
        for i, button in enumerate(buttons):
            if button.text.lower() == variant.lower():
                index = i
        rows = tables[index].xpath('.//tr')
        for row in rows:
            cell = row.xpath('.//td/text()')[0].lower()
            if cell in switch_types:
                return SwitchType[cell]
    
    def _get_switch_type_from_list(self, variant, lis, switch_types):
        for li in lis:
            li_text = li.text.lower()
            switch_type = list(filter(lambda t: t in li_text, switch_types))
            if switch_type:
                return SwitchType[switch_type.pop()]
