import time
from ._common import CommonScraper
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
            self.common_scraper = CommonScraper(self.session, self.product, self.vendor)
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
    
    def _scrape_each_on_page(self):
        i = 0
        while i < len(self._get_cards()) - 1:
            card = self._get_cards()[i]
            card.click()
            time.sleep(1) # wait for product page to load
            self._scrape_and_insert()
            self.driver.back()
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
        options = self._get_options() # first item is title of Select
        options_are_count = self._are_options_count() 
        items = []
        if options and not options_are_count:
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
            self.common_scraper.update_or_insert(**item)
    
    # def _get_details(self, name, option, count):
    #     return dict(
    #         name=self._make_name(name, option, count),
    #         img_url=self._get_img_url(),
    #         price=self._get_price(count, option),
    #         in_stock=self._get_availability(),
    #     )
    
    # def _are_options_count(self):
    #     try:
    #         return self.driver.find_element_by_xpath(
    #             '//label[@for="SingleOptionSelector-0"]'
    #         ).text == "Count"
    #     except NoSuchElementException:
    #         return None
    
    # @staticmethod
    # def _make_name(name, option, count):
    #     if count:
    #         return name
    #     if not option:
    #         return name
    #     return f"{name} {option}"

    # def _get_pagination(self):
    #     pass

    # def _get_options(self):
    #     try:
    #         return Select(self.driver.find_element_by_id('SingleOptionSelector-0'))
    #     except NoSuchElementException:
    #         return None
    
    # def _get_price(self, is_count, count):
    #     try:
    #         price = float(re.search(
    #             r"\d+.\d{1,2}$",
    #             self.driver.find_element_by_class_name("price-item").text
    #         ).group(0))
    #         if is_count:
    #             price = price / int(count)
    #         return price
    #     except NoSuchElementException:
    #         return None
    #     except AttributeError:
    #         return None
    
    # def _get_availability(self):
    #     try:
    #         availability = self.driver.find_element_by_id('AddToCartText-product-template').text
    #     except NoSuchElementException:
    #         return False
    #     if availability == "UNAVAILABLE" or availability == "SOLD OUT":
    #         return False
    #     elif availability == "ADD TO CART":
    #         return True
    #     else:
    #         return False
    
    # def _get_img_url(self):
    #     try:
    #         img = self.driver.find_element_by_class_name("zoomImg")
    #     except NoSuchElementException:
    #         return None
    #     else:
    #         return img.get_attribute("src")