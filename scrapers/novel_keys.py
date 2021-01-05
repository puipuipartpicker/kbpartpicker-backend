# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
from collections import namedtuple
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select

from ._base import BaseScraper
from models.types import ProductType, LayoutType, SizeType
from models import Product, Vendor, VendorProductAssociation


"""
TODO:
1. Extract main logic to Base Class
2. Write tests
3. Add currency
4. Scrape all products on Novelkeys
"""

class NovelKeys(BaseScraper):

    def __init__(self, session, driver, product, name, url):
        super(NovelKeys, self).__init__(session, driver, product, name, url)

    def _get_variants(self, name):
        options = self._get_options() # first item is title of Select
        options_are_count = self._are_options_count() 
        variants = []
        pv_url = self.driver.current_url
        if options and not options_are_count:
            for o in options.options[1:]:
                o.click()    
                variants.append(self._get_details(name, o.text, pv_url))
        elif options and options_are_count:
            o = options.options[1]
            o.click()
            variants.append(self._get_details(name, o.text, pv_url, options_are_count))
        else:
            variants = [self._get_details(name, None, pv_url)]
        return variants

    def _get_details(self, name, option, pv_url, count=False):
        return dict(
            name=self._make_name(name, option, count),
            img_url=self._get_img_url(),
            price=self._get_price(option, count),
            in_stock=self._get_availability(),
            pv_url=pv_url
        )
    
    def _are_options_count(self):
        try:
            return self.driver.find_element_by_xpath(
                '//label[@for="SingleOptionSelector-0"]'
            ).text == "Count"
        except NoSuchElementException:
            return None
    
    @staticmethod
    def _make_name(name, option, count):
        if not count and option:
            return f"{name} {option}"
        else:
            return name

    def _get_options(self):
        try:
            return Select(self.driver.find_element_by_id('SingleOptionSelector-0'))
        except NoSuchElementException:
            return None
    
    def _get_price(self, count, is_count):
        try:
            price = float(re.search(
                r"\d+.\d{1,2}$",
                self.driver.find_element_by_class_name("price-item").text
            ).group(0))
            if self.product.type == ProductType.switch:
                if is_count:
                    price = round(price / int(count), 2)
                return price * 10
            else:
                return price
        except NoSuchElementException:
            return None
        except AttributeError:
            return None
    
    def _get_availability(self):
        try:
            availability = self.driver.find_element_by_id('AddToCartText-product-template').text
        except NoSuchElementException:
            return False
        if availability == "UNAVAILABLE" or availability == "SOLD OUT":
            return False
        elif availability == "ADD TO CART":
            return True
        else:
            return False
    
    def _get_img_url(self):
        try:
            img = self.driver.find_element_by_class_name("zoomImg")
        except NoSuchElementException:
            return None
        else:
            return img.get_attribute("src")
    
    def _get_pages(self):
        pagination = self.driver.find_element_by_class_name("pagination")
        pages = pagination.find_element_by_class_name("pagination__text").text
        return re.findall(r"\d+", pages)