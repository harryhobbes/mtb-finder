import requests
from bs4 import BeautifulSoup
import os.path
import subprocess
import re

ON_UNRAID = False

def getFileLocation():
    return '/mnt/cache/appdata/mtb-finder.txt' if (ON_UNRAID) else 'mtb-finder.txt'

def getCleanPrice(price):
    return price.replace("$","").replace(",","")

def getFormattedPrice(price):
    return f"${float(price):,.2f}"

def writePriceToFile(price):
    priceClean = getCleanPrice(price)

    priceFile = open(getFileLocation(), "w+")
    priceFile.write(priceClean)
    priceFile.close()

def readPriceFromFile():
    price = 0
    filePath = getFileLocation() 

    if (os.path.exists(filePath)):
        priceFile = open(getFileLocation(), 'r')
        if priceFile.mode == 'r':
            price = priceFile.read()
    
    return price

def getDealMessage(price):
    return 'Today\'s price is %s (was %s)' % (price, getFormattedPrice(readPriceFromFile()))

def sendUpdate(price):
    message = getDealMessage(price)

    if (ON_UNRAID):
        command_line = ['/usr/local/emhttp/webGui/scripts/notify', '-i', 'alert', '-s', 'Daily Collosus Price Update', '-d', message]
        process = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=False)
    else:
        print(message)
        
def main():
    page = requests.get('https://www.bikesonline.com.au/2024-polygon-collosus-n9-enduro-mountain-bike')
    #page = requests.get('https://www.bikesonline.com.au/2024-polygon-siskiu-t9-dual-suspension-mountain-bi')

    soup = BeautifulSoup(page.text, 'html.parser')

    price = soup.find(class_='df-price').find(class_='finalprice').text

    sendUpdate(price)
    writePriceToFile(price)

if __name__ == '__main__':
    main()