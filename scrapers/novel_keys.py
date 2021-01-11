# https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
import time
import re
from selenium.webdriver.support.ui import Select
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
        options = self._get_options() # first item is title of Select (eg. Pick a Type)
        options_are_count = self._are_options_count() 
        variants = []
        if self.product.type == ProductType.stabilizer:
            for o in options.options[1:]:
                o.click()
                stabilizer_types = self._get_options(1)
                if stabilizer_types:
                    for t in stabilizer_types.options[1:]:
                        t.click()
                        variants.append(self._get_details(name, o.text, t.text))
                else:
                    variants.append(self._get_details(name, o.text))
        elif options and not options_are_count:
            for o in options.options[1:]:
                o.click()    
                variants.append(self._get_details(name, o.text))
        elif options and options_are_count:
            o = options.options[1]
            o.click()
            variants.append(self._get_details(name, o.text, count=options_are_count))
        else:
            variants = [self._get_details(name)]
        return variants

    def _get_details(self, name, option=None, stab_type=None, count=False):
        product_details = dict()
        pv_details = dict()

        product_details['name'] = self._make_name(self._cleanup_name(name), option, count)
        product_details['product_type'] = self.product.type
        product_details['img_url'] = self._get_img_url()
        if self.product.type == ProductType.stabilizer:
            product_details['size'] = self._get_stabilizer_size(option)
            product_details['stabilizer_type'] = self._get_stabilizer_type(stab_type)
        if self._product_with_layout():
            product_details['layout'] = self._get_layout(name)
        if self._hotswappable_product():
            product_details['hotswap'] = self._is_hotswap(option)

        pv_details['vendor_id'] = self.vendor.id
        pv_details['price'] = self._get_price(option, count)
        pv_details['in_stock'] = self._get_availability()
        pv_details['pv_url'] = self.driver.current_url

        return dict(
            product_details=product_details,
            pv_details=pv_details
        )
    
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
    def _get_options(self, dropdown_id=0):
        return Select(self.driver.find_element_by_id(f'SingleOptionSelector-{dropdown_id}'))
    
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
        # container = self.driver.find_element_by_id("ProductSection-product-template")
        # return container.find_elements_by_tag_name("img")[0].get_attribute("src")
        timeout = 10
        wait = WebDriverWait(self.driver, timeout)
        img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zoomImg")))
        return img.get_attribute("src")
    
    def _get_pages(self):
        pagination = self.driver.find_element_by_class_name("pagination")
        pages = pagination.find_element_by_class_name("pagination__text").text
        return re.findall(r"\d+", pages)

    def _cleanup_name(self, name):
        if self.product.remove:
            return re.sub(self.product.remove, '', name)
        return name

    def _is_hotswap(self, option):
        if option and option.lower() == 'hotswap':
            return True
        else:
            # TODO: fix(stale element reference: element is not attached to the page document)
            #       use a retry() decorator?
            ps = self.driver.find_elements_by_tag_name("p")
            ps = [p.text for p in ps]
            return 'hotswap' in  " ".join(ps).split(" ")
    
    def _get_layout(self, name):
        if self._product_with_layout:
                return self._literal_to_enum(name)
        return None
    
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

    def _product_with_layout(self):
        return (self.product.type == ProductType.case or
                self.product.type == ProductType.pcb or
                self.product.type == ProductType.kit)
    
    def _hotswappable_product(self):
        return (self.product.type == ProductType.pcb or
                self.product.type == ProductType.kit)

