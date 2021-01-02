import re
import time
from .database_action import DatabaseAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException


"""
novelkeys
primekb
thekey.company
kbdfans
kprepublic
cannonkeys
candykeys
ilumkb
dailyclack
"""

class BaseScraper():
    
    def __init__(self, session, driver):
        self.session = session
        self.driver = driver
        self.vendor_url = None
        self.vendor, _ = None
        self.results = []
        self.product = None
        self.product_urls = None

    def run(self):
        for product in self.product_urls:
            self.driver.get(f"{self.vendor_url}{product.url}")
            self.product = product
            self.database_action = DatabaseAction(self.session, self.product, self.vendor)
            self._run()

    def _run(self):
        page_nums = self._get_pagination()
        if page_nums:
            while page_nums[0] != page_nums[-1]:
                self._scrape_each_on_page()
                self._click_page()
                page_nums = self._get_pagination()
            self._scrape_each_on_page()
        else:
            self._scrape_each_on_page()
    
    def _click_page(self):
        (self.driver
            .find_element_by_class_name("pagination")
            .find_element_by_css_selector("a")
            .click())

    def _scrape_each_on_page(self):
        i = 0
        while i < len(self._get_cards()) - 1:
            card = self._get_cards()[i]
            card.click()
            time.sleep(1) # wait for product page to load
            self._scrape_and_insert() # insert product details to database
            self.driver.back() # return to list page
            i += 1
    
    def _get_pagination(self):
        try:
            return self._get_pages()
        except NoSuchElementException:
            return None
    
    def _scrape_and_insert(self):
        name = self._get_product_name()
        if set(self.product.ignore) & set(name.split(' ')):  # ignore products containing bad words
            return
        variants = self._get_variants(name)
        for variant in variants:
            self.database_action.update_or_insert(**variant)
    
    def _get_cards(self):
        return self.driver.find_elements_by_class_name("grid-view-item__link")
    
    def _get_product_name(self):
        return self.driver.find_element_by_class_name("product-single__title").text
