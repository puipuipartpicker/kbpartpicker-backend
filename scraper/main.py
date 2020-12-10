import os
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .scrapers.novel_keys import NovelKeys


def main(session, driver):
    NovelKeys(session, driver).run()

prd = os.environ.get('DATABASE_URL')
if prd:
    engine = create_engine(prd)
    session = sessionmaker(bind=engine)()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
else:
    engine = create_engine('postgres+psycopg2://vi:password@localhost:5432/kbpartpicker')
    session = sessionmaker(bind=engine)()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
timeout = 3
try:
    element_present = EC.presence_of_element_located((By.ID, 'main'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    main(session, driver)
    driver.close()
    session.close()
