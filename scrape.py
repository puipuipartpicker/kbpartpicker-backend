import os

from vendors import nk_vendor, ck_vendor
from config.database import session_maker
from config.driver import driver_maker


def main(session, driver):
    nk_vendor.scraper(session, driver, nk_vendor.config)
    ck_vendor.scraper(session, driver, ck_vendor.config)
    

if __name__ == "__main__":
    driver = driver_maker()
    session = session_maker()
    main(session, driver)
    driver.close()
    session.close()
