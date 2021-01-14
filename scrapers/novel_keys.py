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
        options = self._get_options()
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

    @CatchNoElem()
    def _are_options_count(self):
        return self.driver.find_element_by_xpath(
            '//label[@for="SingleOptionSelector-0"]'
        ).text == "Count"
    
    def _make_name(self, name, option, count):
        if self.product.type == ProductType.stabilizer:
            return name
        else:
            if not count and option:
                return f"{name} {option}"
            else:
                return name

    @CatchNoElem()
    def _get_price(self, count, is_count):
        price_search = re.search(
            r"\d+.\d{1,2}$",
            self.driver.find_element_by_class_name("price-item").text
        )
        if not price_search:
            return None
        price = float(price_search.group(0))
        if self.product.type == ProductType.switch:
            if is_count:
                price = price / int(count)
            return round(price * 10, 2)
        else:
            return price
    
    @CatchNoElem(return_none=False)
    def _get_availability(self):
        availability = self.driver.find_element_by_id('AddToCartText-product-template').text
        if availability == "UNAVAILABLE" or availability == "SOLD OUT":
            return False
        elif availability == "ADD TO CART":
            return True
    
    def _is_hotswap(self, option):
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
