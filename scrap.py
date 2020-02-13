from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import random

proxies = ['1.20.99.178:34781', '12.218.209.130:53281', '110.5.100.130:60996', '117.103.5.186:44825', '190.5.225.178:53570']

proxy = random.choice(proxies)

print(proxy)

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

driver = webdriver.Chrome()
driver.get("https://amazon.com.br")

inputElement = driver.find_element_by_id("twotabsearchtextbox")
inputElement.send_keys("iphone")
inputElement.submit()

html = urlopen(driver.current_url)

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

print(lista)

with open('iphone.csv', 'w', newline='') as mf:
    wr = csv.writer(mf, quoting=csv.QUOTE_ALL)
    for item in lista:
        wr.writerow(item.values())
