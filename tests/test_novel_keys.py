import pytest
import unittest
from pytest import fixture
from unittest.mock import patch

from config.driver import driver_maker
from config.database import session_maker
from scrapers import NovelKeys, DatabaseAction
from vendors import nk_vendor


@fixture
def default_session():
    session = session_maker()
    yield session


@fixture
def default_driver():
    driver = driver_maker()
    yield driver


def mock_update_or_insert(self, product_details, pv_details):
    assert product_details.get('name') is not None
    assert product_details.get('img_url') is not None
    assert pv_details.get('pv_url') is not None
    assert isinstance(pv_details.get('in_stock'), bool)
    if pv_details.get('price') is not None:
        assert isinstance(pv_details.get('price'), float)

@pytest.mark.parametrize("i", list(range(len(nk_vendor.products))), ids=[p.type.name for p in nk_vendor.products])
def test_scrape(default_session, default_driver, i):
    nk = NovelKeys(
        default_session,
        default_driver,
        nk_vendor.products[i],
        nk_vendor.name,
        nk_vendor.url
    )
    with patch.object(DatabaseAction, 'update_or_insert', mock_update_or_insert):
        name = nk.run()
    
    default_session.rollback()
    default_session.close()
    default_driver.close()