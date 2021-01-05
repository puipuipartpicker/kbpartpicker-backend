import pytest
import unittest
from unittest.mock import patch

from config.database import session
from config.driver import driver
from scrapers import NovelKeys, DatabaseAction
from vendors import nk_vendor


def mock_update_or_insert(self, name, img_url, price, in_stock, pv_url):
    assert name is not None
    assert img_url is not None
    assert pv_url is not None
    assert isinstance(in_stock, bool)
    if price is not None:
        assert isinstance(price, float)

class TestNovelKeys(unittest.TestCase):

    def setUp(self): 
        self.session = session
        self.driver = driver

    def testScrapeSwitches(self):
        nk = NovelKeys(
            self.session,
            self.driver,
            nk_vendor.products[0],
            nk_vendor.name,
            nk_vendor.url
        )
        with patch.object(DatabaseAction, 'update_or_insert', mock_update_or_insert):
            name = nk.run()
    
    def tearDown(self):
        self.session.rollback()
        self.session.close()
        self.driver.close()