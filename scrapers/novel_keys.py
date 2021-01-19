# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

from ._base import BaseScraper
from app.models.types import ProductType, LayoutType, SizeType, StabilizerType
from app.models import Product, Vendor, VendorProductAssociation
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

    def __init__(self, session, driver, product, name, url):
        super(NovelKeys, self).__init__(session, driver, product, name, url)

    def _get_variants(self, name):
        variants = []
        drop_downs = self._get_options_and_type()
        if not drop_downs:
            return [self._get_details(name)]

        count_options = drop_downs.get("Count")
        type_options = (
            drop_downs.get("Type") or
            drop_downs.get("Kit") or
            drop_downs.get("Color") or
            drop_downs.get("Weight") or
            (drop_downs.get("Style") if self.product.type != ProductType.stabilizer else None)
        )
        size_options = drop_downs.get("Size")
        stab_type_options = drop_downs.get("Style")

        if count_options and not type_options:
            count_options[0].click()  # only need the first option to calculate per item price
            return [self._get_details(name, count_option=count_options[0].text)]
        elif type_options:
            for t in type_options:
                t.click()
                if count_options:
                    count_options[0].click()
                    variants.append(self._get_details(name, type_option=t.text, count_option=count_options[0].text))
                else:
                    variants.append(self._get_details(name, type_option=t.text))
            return variants
        elif size_options:
            for si in size_options:
                si.click()
                if stab_type_options:
                    for st in stab_type_options:
                        st.click()
                        variants.append(self._get_details(name, stab_size=si.text, stab_type=st.text))
                else:
                    variants.append(self._get_details(name, stab_size=si.text))
            return variants

    def _make_name(self, name, type_option):
        return f"{name} {type_option}" if type_option else name

    @CatchNoElem()
    def _get_price(self, count):
        price_search = re.search(
            r"\d+.\d{1,2}$",
            self.driver.find_element_by_class_name("price-item").text
        )
        if not price_search:
            return None
        price = float(price_search.group(0))
        if (self.product.type == ProductType.switch) and count:
            price = price / (int(count) / 10)
            # return round(price * 10, 2)
        return round(price, 2)
    
    @CatchNoElem(return_none=False)
    def _get_availability(self):
        availability = self.driver.find_element_by_id('AddToCartText-product-template').text
        if availability == "UNAVAILABLE" or availability == "SOLD OUT":
            return False
        elif availability == "ADD TO CART":
            return True
    
    def _get_hotswappability(self, option):
        if option and option.lower() == 'hotswap':
            return True
        else:
            # TODO: fix(stale element reference: element is not attached to the page document)
            #       use a retry() decorator?
            ps = self.driver.find_elements_by_tag_name("p")
            ps = [p.text for p in ps]
            return 'hotswap' in  " ".join(ps).split(" ")
    
    def _get_stabilizer_size(self, size):
        # TODO: abstract logic to base class
        return {
            "7u":SizeType.seven_u,
            "2u":SizeType.two_u,
            "6.25u":SizeType.six_point_25_u
        }.get(size)

    def _get_stabilizer_type(self, type_name):
        if not type_name:
            return None
        formatted = '_'.join(type_name.lower().split(' '))
        return StabilizerType[formatted]
