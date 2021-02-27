import os

from selenium import webdriver 


def driver_maker():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=chrome_options)
