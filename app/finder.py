import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import os.path
import subprocess
import re

def get_clean_price(price):
    return price.replace("$","").replace(",","")
        
def find_deal(target_url, css_selector):
    price = None

    try:
        # Create a UserAgent object
        ua = UserAgent()
        # Set a random User-Agent header in the request
        headers = {'User-Agent': ua.random}
        page = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        element = soup.css.select_one(css_selector)
        if element:
            price = element.text
        else:
            print('Price grab failed. Likely dynamic content. Trying advanced Finder')
            price = find_dynamic_deal(target_url, css_selector)
    except:
        print('Exception thrown: Issue with find_deal function')

    return price
        
def find_dynamic_deal(target_url, css_selector):
    price = None

    try:
        # Create a UserAgent object
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        # Don't run in sandbox mode (comes with security issues, but good for debugging)
        options.add_argument('--no-sandbox')

        # Use /tmp instead of /dev/shm due to storage issues
        options.add_argument('--disable-dev-shm-usage')
        
        # Set the Chrome user director
        #user_dir = os.environ["CHROMIUM_USER_DIR"]
        #options.add_argument(f'--user-data-dir={user_dir}')

        # Set a random User-Agent header in the request
        user_agent = ua.random
        options.add_argument(f'--user-agent={user_agent}')

        #options.binary_location = os.environ["CHROMIUM_BINARY"]
        driver = webdriver.Chrome(options=options)

        driver.get(target_url)

        # this is just to ensure that the page is loaded 
        time.sleep(5)  

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        element = soup.css.select_one(css_selector)
        price = element.text if element else None
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)
        print('Price grab failed. Likely an issue with the source or CSS selector')

    return price