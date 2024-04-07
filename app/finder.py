import requests
from bs4 import BeautifulSoup
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
    page = requests.get(target_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    price = soup.css.select_one(css_selector).text

    return price