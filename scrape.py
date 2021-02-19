import os
from datetime import date

from app.models import Product
from vendors import nk_vendor, ck_vendor
from config.database import session_maker
from config.driver import driver_maker


def updated_today():
    last_product = Product.query.order_by(Product.updated_at.desc()).first()
    return last_product.updated_at.date() == date.today()


def main(session, driver):
    nk_vendor.scraper(session, driver, nk_vendor.config)
    ck_vendor.scraper(session, driver, ck_vendor.config)
    

if __name__ == "__main__":
    if not updated_today():
        print("Scraping START! 🏁")
        driver = driver_maker()
        session = session_maker()
        main(session, driver)
        driver.close()
        session.close()
        print("Done scraping! 🎉")
    else:
        print("Vendors already scraped today! 🎉")
        print("Skipping...")
