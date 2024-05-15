import requests
from bs4 import BeautifulSoup


page = requests.get("https://www.jumia.co.ke/samsung-galaxy-a04e-lte-6.5-32gb-3gb-ram-dual-sim-5000mah-black-2yrs-wrty-196740671.html")
soup = BeautifulSoup(page.content, 'html.parser')

product_data = soup.select("div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul, div[class*='markup -mhm -pvl -oxa -sc'] img")

for data in product_data:
    if data.name == "img":
        print(data["data-src"])
    else:
        print(data.text)



