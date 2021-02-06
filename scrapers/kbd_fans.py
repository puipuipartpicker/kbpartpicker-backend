# import time
# import re
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 

from ._base import BaseScraper
# from app.models.types import ProductType, KeyboardFormFactor, StabilizerSize, StabilizerType
# from app.models import Product, Vendor, VendorProductAssociation
# from utils.catch_noelem_exception import CatchNoElem
# from utils.regex_dict import RegexDict


class KBDFans(BaseScraper):

    def __init__(self, session, driver, product, name, url):
        super(KBDFans, self).__init__(session, driver, product, name, url)
