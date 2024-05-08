import requests
from bs4 import BeautifulSoup
import os
from parsers import Parser
import category_links

headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}

page = requests.get('https://www.kilimall.co.ke/search-result?id=968&form=category&ctgName=Shoes', headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

items = soup.find_all("div", class_="product-item")
for item in items:
    print(item)

btn = soup.find("span", class_="arrow")
print(btn)
