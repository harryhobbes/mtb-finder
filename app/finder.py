import requests
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
    price = '0.00'

    try:
        page = requests.get(target_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        price = soup.css.select_one(css_selector).text
    except:
        print('Price grab failed. Likely dynamic content. Trying advanced Finder')
        price = find_dynamic_deal(target_url, css_selector)

    return price
        
def find_dynamic_deal(target_url, css_selector):
    price = '0.00'

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver = webdriver.Chrome(options=options)

        driver.get(target_url)

        # this is just to ensure that the page is loaded 
        time.sleep(5)  

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        price = soup.css.select_one(css_selector).text
    except:
        print('Price grab failed. Likely an issue with the source or CSS selector')

    return price