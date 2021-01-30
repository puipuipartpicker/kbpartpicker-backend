import os

from vendors import nk_vendor, ck_vendor
from config.database import session_maker
from config.driver import driver_maker


def main(session, driver):
    # for product in nk_vendor.products:
    #     nk_vendor.scraper(session, driver, product, nk_vendor.name, nk_vendor.url).run()
    for product in ck_vendor.products:
        ck_vendor.scraper(session, driver, product, ck_vendor.name, ck_vendor.url).run()

if __name__ == "__main__":
    driver = driver_maker()
    session = session_maker()
    main(session, driver)
    driver.close()
    session.close()
