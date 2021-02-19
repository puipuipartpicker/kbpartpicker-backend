import os

from selenium import webdriver 


mode = os.environ.get('MODE')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_prefs = {}
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_options.experimental_options["prefs"] = chrome_prefs

def driver_maker():
    if mode == 'prd':
        print('prd')
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    else:
        print('dev')
        return webdriver.Chrome(options=chrome_options)
