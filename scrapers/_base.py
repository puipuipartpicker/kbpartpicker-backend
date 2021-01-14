import re
import time
from .database_action import DatabaseAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

from app.models import Vendor
from app.models.types import LayoutType
from utils.regex_dict import RegexDict


"""
[-]novelkeys
[ ]primekb
[ ]thekey.company
[ ]kbdfans
[ ]kprepublic
[-]cannonkeys
[ ]candykeys
[ ]ilumkb
[ ]dailyclack
[ ]prototypist
"""

# TODO: Consider adding spring weight column

class BaseScraper():
    
    def __init__(self, session, driver, product, name, url):
        self.session = session
        self.driver = driver
        self.product = product
        self.vendor_url = url
        self.vendor, _ = Vendor.get_or_create(self.session, name=name, url=url)
        self.database_action = DatabaseAction(self.session)

    def run(self):
        self.driver.get(f"{self.vendor_url}{self.product.url}")
        timeout = 3
        try:
            element_present = EC.presence_of_element_located((By.ID, "Collection"))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
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
        if self.product.ignore:
            if set(self.product.ignore) & set(name.lower().split(' ')):  # ignore products containing bad words
                return
        if self.product.include:
            if not set(self.product.include) & set(name.lower().split(' ')):  # include only products with words in name
                return
        variants = self._get_variants(name)
        for variant in variants:
            self.database_action.update_or_insert(**variant)
    
    def _get_cards(self):
        return self.driver.find_elements_by_class_name("grid-view-item__link")
    
    def _get_product_name(self):
        return self.driver.find_element_by_class_name("product-single__title").text

    @staticmethod
    def _literal_to_enum(literal):
        reg_dict = RegexDict()
        reg_dict[re.compile(r"4[0-9]|Forty", re.I)] = LayoutType.forty_percent
        reg_dict[re.compile(r"60|Sixty", re.I)] = LayoutType.sixty_percent
        reg_dict[re.compile(r"6[5-9]|Sixty-Five|Sixtyfive", re.I)] = LayoutType.sixtyfive_percent
        reg_dict[re.compile(r"7[0-9]|Seventy-Five|Seventyfive", re.I)] = LayoutType.seventyfive_percent
        reg_dict[re.compile(r"8[0-9]|TKL|Tenkeyless", re.I)] = LayoutType.tenkeyless
        try:
            return reg_dict[literal]
        except KeyError:
            return None