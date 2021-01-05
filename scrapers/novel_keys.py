# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
from selenium.webdriver.support.ui import Select

from ._base import BaseScraper
from models.types import ProductType, LayoutType, SizeType
from models import Product, Vendor, VendorProductAssociation
from utils.catch_noelem_exception import CatchNoElem


"""
TODO:
2. Write tests
3. Add currency (Create form for backend API to fill out manually)
4. Scrape all products on Novelkeys
"""

class NovelKeys(BaseScraper):

    def __init__(self, session, driver, product, name, url):
        super(NovelKeys, self).__init__(session, driver, product, name, url)

    def _get_variants(self, name):
        options = self._get_options() # first item is title of Select (eg. Pick a Type)
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
    
    @CatchNoElem()
    def _are_options_count(self):
        return self.driver.find_element_by_xpath(
            '//label[@for="SingleOptionSelector-0"]'
        ).text == "Count"
    
    @staticmethod
    def _make_name(name, option, count):
        if not count and option:
            return f"{name} {option}"
        else:
            return name

    @CatchNoElem()
    def _get_options(self):
        return Select(self.driver.find_element_by_id('SingleOptionSelector-0'))
    
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
    
    @CatchNoElem(return_none=False)
    def _get_img_url(self):
        container = self.driver.find_element_by_id("ProductSection-product-template")
        return container.find_elements_by_tag_name("img")[0].get_attribute("src")
    
    def _get_pages(self):
        pagination = self.driver.find_element_by_class_name("pagination")
        pages = pagination.find_element_by_class_name("pagination__text").text
        return re.findall(r"\d+", pages)
