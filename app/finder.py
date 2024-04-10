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

def send_update(message):
    if (current_app.config['ON_UNRAID']):
        command_line = ['/usr/local/emhttp/webGui/scripts/notify', '-i', 'alert', '-s', 'Daily Collosus Price Update', '-d', message]
        process = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=False)
    else:
        print(message)
        
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
        # Set a random User-Agent header in the request
        user_agent = ua.random
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument(f'--user-agent={user_agent}')
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver = webdriver.Chrome(options=options)

        driver.get(target_url)

        # this is just to ensure that the page is loaded 
        time.sleep(5)  

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        element = soup.css.select_one(css_selector)
        price = element.text if element else None
    except:
        print('Price grab failed. Likely an issue with the source or CSS selector')

    return price