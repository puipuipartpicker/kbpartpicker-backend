import re
import time
from .database_action import DatabaseAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 

from app.models import Vendor
from app.models.types import LayoutType, ProductType
from utils.regex_dict import RegexDict
from utils.catch_noelem_exception import CatchNoElem


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
# TODO: Refactor to match all child scrapers (add raise NotImplementedError)

class BaseScraper():
    
    def __init__(self, session, driver, product, name, url):
        self.session = session
        self.driver = driver
        self.product = product
        self.vendor_url = url
        self.vendor, _ = Vendor.get_or_create(self.session, name=name, url=url)
        self.database_action = DatabaseAction(self.session)
        self._img_class_name = ""

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
                self._click_next_page()
                page_nums = self._get_pagination()
            self._scrape_each_on_page()
        else:
            self._scrape_each_on_page()
    
    def _click_next_page(self):
        self.driver.find_elements_by_css_selector(".pagination a")[-1].click()

    def _scrape_each_on_page(self):
        i = 0
        while i < len(self._get_cards()) - 1:
            card = self._get_cards()[i]
            card.click()
            time.sleep(1) # wait for product page to load
            self._scrape_and_insert() # insert product details to database
            self.driver.back() # return to list page
            i += 1
    
    @CatchNoElem()
    def _get_pagination(self):
        # pagination = self.driver.find_element_by_class_name("pagination")
        pages = self.driver.find_element_by_class_name("pagination__text").text
        return re.findall(r"\d+", pages)

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

    def _get_variants(self, name):
        raise NotImplementedError

    def _get_details(
            self, name, type_option=None, count_option=None, stab_type=None, stab_size=None
        ):
        product_details = dict()
        pv_details = dict()

        product_details['name'] = self._make_name(self._cleanup_name(name), type_option)
        product_details['product_type'] = self.product.type
        product_details['img_url'] = self._get_img_url()
        if self.product.type == ProductType.stabilizer:
            product_details['size'] = self._get_stabilizer_size(stab_size)
            product_details['stabilizer_type'] = self._get_stabilizer_type(stab_type)
        if self._product_with_layout():
            product_details['layout'] = self._get_layout(name)
        if self._hotswappable_product():
            product_details['hotswap'] = self._get_hotswappability(type_option)

        pv_details['vendor_id'] = self.vendor.id
        pv_details['price'] = self._get_price(count_option)
        pv_details['in_stock'] = self._get_availability()
        pv_details['pv_url'] = self.driver.current_url

        return dict(
            product_details=product_details,
            pv_details=pv_details
        )

    def _get_options_and_type(self):
        drop_downs = dict()
        options = self.driver.find_elements_by_class_name("single-option-selector")
        if not options:
            return None
        for i, option in enumerate(options):
            option_type = self.driver.find_element_by_xpath(
                f'//label[@for="SingleOptionSelector-{i}"]'
            ).text
            drop_down_options = Select(option).options
            drop_downs[option_type] = (
                drop_down_options[1:]
                if "pick a" in drop_down_options[0].text.lower()
                else drop_down_options
            )
        return drop_downs

    def _get_cards(self):
        return self.driver.find_elements_by_class_name("grid-view-item__link")
    
    def _get_product_name(self):
        return self.driver.find_element_by_class_name("product-single__title").text

    def _get_layout(self, name):
        if self._product_with_layout:
            return self._literal_to_enum(name)
        return None

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

    def _cleanup_name(self, name):
        if self.product.remove:
            return re.sub(self.product.remove, '', name)
        return name

    def _product_with_layout(self):
        return (self.product.type == ProductType.case or
                self.product.type == ProductType.pcb or
                self.product.type == ProductType.kit)

    def _hotswappable_product(self):
        return (self.product.type == ProductType.pcb or
                self.product.type == ProductType.kit)

    @CatchNoElem(return_none=False)
    def _get_img_url(self):
        # container = self.driver.find_element_by_id("ProductSection-product-template")
        # return container.find_elements_by_tag_name("img")[0].get_attribute("src")
        timeout = 10
        wait = WebDriverWait(self.driver, timeout)
        img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'feature-row__image')))
        return img.get_attribute("src")

    def _make_name(self, name, type_option):
        return f"{name} {type_option}" if type_option else name

    @CatchNoElem(return_none=False)
    def _get_availability(self):
        availability = self.driver.find_element_by_id('AddToCartText-product-template').text
        if availability == "UNAVAILABLE" or availability == "SOLD OUT":
            return False
        elif availability == "ADD TO CART":
            return True

    def _get_hotswappability(self, option):
        raise NotImplementedError

    def _get_stabilizer_size(self, size):
        # TODO: abstract logic to base class
        # return {
        #     "7u":SizeType.seven_u,
        #     "2u":SizeType.two_u,
        #     "6.25u":SizeType.six_point_25_u
        # }.get(size)
        raise NotImplementedError

    def _get_stabilizer_type(self, type_name):
        raise NotImplementedError