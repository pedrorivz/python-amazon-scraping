from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import random

site = 'https://amazon.com.br'
textToSearch = 'iphone'

def randomProxy(fileName):
    lines = open(fileName).read().splitlines()
    return random.choice(lines)

def proxyToUse():
    proxy = randomProxy('proxy.txt') 
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    desired_capabilities['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }

def navBrowser():
    proxyToUse()
    driver = webdriver.Chrome()
    driver.get(site)

    inputElement = driver.find_element_by_id("twotabsearchtextbox")
    inputElement.send_keys(textToSearch)
    inputElement.submit()
    return urlopen(driver.current_url)

def parseHtml():
    html = navBrowser()
    span = BeautifulSoup(html.read(), "html5lib")
    productList = []
    divs = span.findAll("div", {"class":"a-section a-spacing-medium"})

    for span in divs:
        nameTag = span.find("span", {"class":["a-size-base-plus", "a-size-medium"]})
        priceTag = span.find("span", {"class":"a-offscreen"})

        if nameTag and priceTag:
                productList.append({
                    'Product':nameTag.getText(),
                    'Price':priceTag.getText()
                    })

    return productList

def saveToCsv():
    productList = parseHtml()
    with open(textToSearch+'.csv', 'w', newline='') as myFile:
        writeLines = csv.writer(myFile, quoting=csv.QUOTE_ALL)
        for item in productList:
            writeLines.writerow(item.values())





if __name__ == '__main__':
   saveToCsv()
