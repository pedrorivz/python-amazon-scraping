from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

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
    wr.writerow(lista)
