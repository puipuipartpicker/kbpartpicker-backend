import os

from vendors import nk_vendor
from config.database import session
from config.driver import driver


def main(session, driver):
    for product in nk_vendor.products:
        nk_vendor.scraper(session, driver, product, nk_vendor.name, nk_vendor.url).run()

if __name__ == "__main__":
    main(session, driver)
    driver.close()
    session.close()
