import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Jumia"]

page = requests.get("https://www.jumia.co.ke/thinkpad-x260-intel-core-i5-8gb-ram-256gb-ssd-12.5-refurbished-lenovo-mpg1813988.html").content

soup = BeautifulSoup(page, "html.parser")

product_description = soup.select("div.markup.-mhm.-pvl.-oxa.-sc")
for p in product_description:
    description =  p.text




