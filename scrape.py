import os
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vendors import nk_vendor
from config.database import session


def main(session, driver):
    for product in nk_vendor.products:
        nk_vendor.scraper(session, driver, product, nk_vendor.name, nk_vendor.url).run()

if __name__ == "__main__":
    mode = os.environ.get('MODE')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    if mode == 'prd':
        print('prd')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    else:
        print('dev')
        driver = webdriver.Chrome(options=chrome_options)
    main(session, driver)
    driver.close()
    session.close()
