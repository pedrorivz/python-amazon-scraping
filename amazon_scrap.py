from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import random

def random_proxy(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def proxyToUse():
    proxy = random_proxy('proxy.txt') 
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
    driver.get("https://amazon.com.br")

    inputElement = driver.find_element_by_id("twotabsearchtextbox")
    inputElement.send_keys("iphone")
    inputElement.submit()
    return urlopen(driver.current_url)

def parseHtml():
    html = navBrowser()
    span = BeautifulSoup(html.read(), "html5lib")
    lista = []
    divs = span.findAll("div", {"class":"a-section a-spacing-medium"})

    for span in divs:
        nametag = span.find("span", {"class":"a-size-base-plus"})
        pricetag = span.find("span", {"class":"a-offscreen"})

        if nametag and pricetag:
                lista.append({
                    'Product':nametag.getText(),
                    'Price':pricetag.getText()
                    })
    return lista

def saveToCsv():
    lista = parseHtml()
    with open('iphone.csv', 'w', newline='') as mf:
        wr = csv.writer(mf, quoting=csv.QUOTE_ALL)
        for item in lista:
            wr.writerow(item.values())





if __name__ == '__main__':
   saveToCsv()
