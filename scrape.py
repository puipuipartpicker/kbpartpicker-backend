import os
from datetime import date

from app.models import Product, VendorProductAssociation
from vendors import nk_vendor, ck_vendor
from config.database import session_maker
from config.driver import driver_maker


def updated_today(last_vendor):
    if pv := VendorProductAssociation.query.order_by(
            VendorProductAssociation.updated_at.desc()
        ).first():
        if pv.vendor.name == last_vendor.config.name:
            return pv.updated_at.date() == date.today()
        else:
            return False
    else:
        return False


def main(session, driver):
    vendors = [nk_vendor, ck_vendor]
    if not updated_today(vendors[-1]):
        print("Scraping START! 🏁")
        for vendor in vendors:
            vendor.scraper(session, driver, vendor.config)
        print("Done scraping! 🎉")
    else:
        print("Vendors already scraped today! 🎉")
        print("Skipping...")


if __name__ == "__main__":
    driver = driver_maker()
    session = session_maker()
    main(session, driver)
    driver.close()
    session.close()
