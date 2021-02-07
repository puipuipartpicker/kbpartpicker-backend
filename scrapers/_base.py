import re
import time
import inflect
from .database_action import DatabaseAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 

from app.models import Vendor
from app.models.types import KeyboardFormFactor, ProductType, StabilizerSize, KeyboardLayout
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
    
    def __init__(self, session, driver, vendor_config):
        self.session = session
        self.driver = driver
        self.vendor_config = vendor_config
        self.vendor, _ = Vendor.get_or_create(self.session, name=vendor_config.name, url=vendor_config.url)
        self.database_action = DatabaseAction(self.session)
        self._img_class_name = ""
        self.inflect_engine = inflect.engine()

        for product in vendor_config.products:
            self.product = product
            self.driver.get(f"{vendor_config.url}{product.url}")
            timeout = 3
            try:
                element_present = EC.presence_of_element_located((By.ID, "Collection"))
                WebDriverWait(self.driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            self.run()

    def run(self):
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
        while i < len(self._get_cards()):
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
        variant_fields = self._get_variant_fields(name)
        for v in variant_fields:
            details = self._get_details(**v)
            self.database_action.update_or_insert(*details)

    def _get_variant_fields(self, name):
        raise NotImplementedError

    def _get_details(
            self, name='', type_option='', count_option=None, stab_type=None, stab_size=None
        ):
        product_details = dict(
            name=self._make_name(self._cleanup_name(name), type_option),
            product_type=self.product.type,
            img_url=self._get_img_url(),
            stabilizer_size=self._get_stabilizer_size(stab_size),
            stabilizer_type=self._get_stabilizer_type(stab_type),
            keyboard_form_factor=self._get_keyboard_profile(name),
            keyboard_layout=self._get_keyboard_layout(type_option),
            hotswap=self._get_hotswappability(type_option),
            switch_type=self._get_switch_type(self._singularize(type_option))
        )
        pv_details = dict(
            vendor_id=self.vendor.id,
            price=self._get_price(count_option),
            in_stock=self._get_availability(),
            url=self.driver.current_url
        )
        return product_details, pv_details

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

    def _get_keyboard_profile(self, name):
        if not self._needs_keyboard_form_factor:
            return None
        return KeyboardFormFactor.get_from_literal(name)
    
    def _get_keyboard_layout(self, type_option):
        if not self._needs_keyboard_form_factor():
            return None
        keyboard_layouts = [k.name for k in KeyboardLayout]
        option_name = type_option.lower()
        if option_name in keyboard_layouts:
            return KeyboardLayout[option_name]
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
    
    def _cleanup_name(self, name):
        if self.product.remove:
            return re.sub(self.product.remove, '', name)
        return name.rstrip()

    def _needs_keyboard_form_factor(self):
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

    def _make_name(self, name, type_option=''):
        name = (
            f"{self._singularize(name)} {self._singularize(type_option)}"
        ).rstrip()
        if self.product.type == ProductType.lube:
            return self._get_lube_name(name)
        return name

    def _singularize(self, text):
        sing_text = self.inflect_engine.singular_noun(text)
        if sing_text:
            return sing_text
        else:
            return text

    @CatchNoElem(return_none=False)
    def _get_availability(self):
        availability = self.driver.find_element_by_id('AddToCartText-product-template').text
        if availability == "UNAVAILABLE" or availability == "SOLD OUT":
            return False
        elif availability == "ADD TO CART":
            return True

    def _get_hotswappability(self, option):
        if not self._hotswappable_product():
            return False
        if option and option.lower() == 'hotswap':
            return True
        else:
            # TODO: fix(stale element reference: element is not attached to the page document)
            #       use a retry() decorator?
            ps = self.driver.find_elements_by_tag_name("p")
            ps = [p.text.lower() for p in ps]
            lis = self.driver.find_elements_by_tag_name("li")
            lis = [li.text.lower() for li in lis]
            return any([
                    'hotswap' in  " ".join(ps).split(" "),
                    'hotswap' in  " ".join(lis).split(" "),
                ])

    def _get_stabilizer_size(self, size):
        if not (self.product.type != ProductType.stabilizer and size):
            return None
        return {
            "7u":StabilizerSize.seven_u,
            "2u":StabilizerSize.two_u,
            "6.25u":StabilizerSize.six_point_25_u
        }.get(size)

    def _get_stabilizer_type(self, type_name):
        raise NotImplementedError

    def _get_switch_type(self, variant):
        raise NotImplementedError

    def _get_lube_name(self, name):
        groups = re.search(r"(\d{3,})\s*g?(\d)?", name, re.I).groups()
        if "krytox" in name.lower():
            grade = f"g{groups[1]}" if groups[1] else ""
            return f"Krytox {groups[0]}{grade}"
        elif "tribosys" in name.lower():
            return f"Tribosys {groups[0]}"
