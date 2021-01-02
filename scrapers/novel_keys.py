# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
import time
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


Product = namedtuple('Product', 'url type ignore include')
Products = [
    Product('switches', ProductType.switch, ['sample', 'big'], []),
    Product('keycaps', ProductType.keyset, [], []),
    Product('keyboards', ProductType.kit, [], []),
    Product('diy-kits', ProductType.pcb, [], ['pcb']),
    Product('diy-kits', ProductType.kit, [], ['kit']),
    Product('miscellaneous', ProductType.stabilizer, [], ['stabilizers']),
    Product('miscellaneous', ProductType.lube, [], ['lubricants']),
    Product('miscellaneous', ProductType.film, [], ['films']),
    Product('miscellaneous', ProductType.spring, [], ['springs']),
    Product('miscellaneous', ProductType.tool, [], ['puller, opener'])
]


class NovelKeys():

    def __init__(self, session, driver):
        self.session = session
        self.driver = driver
        self.vendor_url = "https://novelkeys.xyz/collections/" 
        self.vendor, _ = Vendor.get_or_create(self.session, name='NovelKeys', url=self.vendor_url)
        self.results = []
        self.product = None

    def run(self):
        for product in Products:
            self.driver.get(f"{self.vendor_url}{product.url}")
            self.product = product
            self.base_scraper = BaseScraper(self.session, self.product, self.vendor)
            self._run()

    def _run(self):
        page_nums = self._get_pagination()
        if page_nums:
            while page_nums[0] != page_nums[-1]:
                self._scrape_each_on_page()
                (self.driver
                    .find_element_by_class_name("pagination")
                    .find_element_by_css_selector("a")
                    .click())
                page_nums = self._get_pagination()
            self._scrape_each_on_page()
        else:
            self._scrape_each_on_page()
    
    def _scrape_each_on_page(self):
        cards = self.driver.find_elements_by_class_name("grid-view-item__link")
        i = 0
        while i < len(cards) - 1:
            card = self.driver.find_elements_by_class_name("grid-view-item__link")[i]
            name = card.find_element_by_class_name("visually-hidden").text
            if self.product.ignore:
                if set(self.product.ignore) & set(name.lower().split(' ')):  # ignore products containing bad words
                    i += 1
                    continue
            if self.product.include:
                if not set(self.product.include) & set(name.lower().split(' ')):  # include only products with words in name
                    i += 1
                    continue
            card.click()
<<<<<<< HEAD
            time.sleep(1) # let page load before scrape
=======
            time.sleep(10)
>>>>>>> main
            self._scrape_and_insert()
            i += 1
            self.driver.back()
    
    def _scrape_and_insert(self):
        name = self.driver.find_element_by_class_name("product-single__title").text
<<<<<<< HEAD
        items = []
        options = self._get_options()
        if options:
=======
        options = self._get_options()
        options_are_count = self._are_options_count() # first item is "Pick"
        items = []
        if options and not options_are_count:
>>>>>>> main
            for o in options.options[1:]:
                o.click()    
                items.append(self._get_details(name, o.text, options_are_count))
        elif options and options_are_count:
            o = options.options[1]
            o.click()
            items.append(self._get_details(name, o.text, options_are_count))
        else:
            items = [self._get_details(name, None, False)]
        for item in items:
            print(item)
            self.base_scraper.update_or_insert(**item)
    
    def _get_details(self, name, option, count):
        return dict(
            name=self._make_name(name, option, count),
            img_url=self._get_img_url(),
            price=self._get_price(count, option),
            in_stock=self._get_availability(),
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
        if count:
            return name
        if not option:
            return name
        return f"{name} {option}"

    def _get_pagination(self):
        try:
            pagination = self.driver.find_element_by_class_name("pagination")
        except NoSuchElementException:
            return None
        
        pages = pagination.find_element_by_class_name("pagination__text").text
        return re.findall(r"\d+", pages)

    def _get_options(self):
        try:
            return Select(self.driver.find_element_by_id('SingleOptionSelector-0'))
        except NoSuchElementException:
            return None
    
    def _get_price(self, is_count, count):
        try:
            price = float(re.search(
                r"\d+.\d{1,2}$",
                self.driver.find_element_by_class_name("price-item").text
            ).group(0))
            if is_count:
                price = price / int(count)
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