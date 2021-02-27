import pytest
import unittest
from pytest import fixture
from unittest.mock import patch

from config.driver import driver_maker
from config.database import session_maker
from scrapers import NovelKeys, DatabaseAction
from vendors import nk_vendor
from models.types import ProductType


@fixture
def default_session():
    session = session_maker()
    yield session


@fixture
def default_driver():
    driver = driver_maker()
    yield driver


def test_scrape(default_session, default_driver):
    assert True
    default_session.close()
    default_driver.close()
