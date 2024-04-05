import requests
from bs4 import BeautifulSoup
import os.path
import subprocess
import re

def getCleanPrice(price):
    return price.replace("$","").replace(",","")

def getFormattedPrice(price):
    return f"${float(price):,.2f}"

def sendUpdate(price):
    message = getDealMessage(price)

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