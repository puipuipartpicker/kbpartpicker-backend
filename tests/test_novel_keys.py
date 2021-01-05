import pytest
import unittest

from config.database import session

class TestNovelKeys(unittest.TestCase):

    @classmethod
    def setup(cls): 
        cls.session = session
    
    @classmethod
    def teardown(cls):
        cls.session.rollback()
        cls.session.close()