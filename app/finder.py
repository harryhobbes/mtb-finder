import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import os.path
import subprocess
import re

# Check the element and confirm it has valid text for our records
def get_valid_element_text(element):
    price = None

    try:
        if (element):
            price = element.text.rstrip()
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)
        print('Exception throw: Likely not a string or value we can use')
        
    return price

# Amount can be a string like $400.00 or 56 or $3,450 or <a nested div> or "just some text"
# We want a float or a False back
def get_amount(value):
    # Check if the value is an integer or a float
    if isinstance(value, (int, float)):
        return float(value) if value > 0 else False

    # Check if the value is a string
    if isinstance(value, str):
        # Remove any dollar signs and commas
        value = re.sub(r'[^\d.-]', '', value)
        try:
            amount = float(value)
            return amount if amount > 0 else False
        except ValueError:
            return False

    return False
        
def find_deal(target_url, css_selector):
    price = None

    try:
        # Create a UserAgent object
        ua = UserAgent()
        # Set a random User-Agent header in the request
        headers = {'User-Agent': ua.random}
        page = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Get an element from the HTML
        try:
            price = get_amount(get_valid_element_text(soup.css.select_one(css_selector)))
        except Exception as error:
            print('Likely using advanced features: ', type(error).__name__, "-", error)

        if price == None or not price:
            print('Price grab failed. Likely dynamic content. Trying advanced Finder')
            price = find_dynamic_deal(target_url, css_selector)
    except Exception as error:
        price = None
        print("An exception occurred:", type(error).__name__, "–", error)
        print('Exception thrown: Issue with find_deal function')

    return price

def get_dynamic_browser():
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

    return driver

def look_and_wait(driver, css_selector):
    price = None
    still_sleeping = 5

    while price is None and still_sleeping:
        # try javascript to get the amount
        dirty_js_return_val = driver.execute_script(f"return {css_selector};")
        price = get_amount(dirty_js_return_val)

        if price is None:
            # Wait a second to ensure the page is loaded 
            time.sleep(1)
        
        still_sleeping -= 1

    print("Sleep count: ", 5 - still_sleeping)
    return price
        
def find_dynamic_deal(target_url, css_selector):
    try:
        driver = get_dynamic_browser()
        driver.get(target_url)

        price = look_and_wait(driver, css_selector)

        driver.quit()
    except Exception as error:
        price = None
        print("An exception occurred:", type(error).__name__, "–", error)
        print('Price grab failed. Likely an issue with the source or CSS selector')

    return price