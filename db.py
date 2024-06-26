from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bson.objectid import ObjectId  # Ensure this import for ObjectId


class ProductsLocator:
    LOCATOR = "article[class*='prd _fb col c-prd']"
    DESCRIPTION_LOCATOR = "div[class*='markup -mhm -pvl -oxa -sc']"


class ProductsInformationLocator:
    NAME = "div.info h3.name"
    DESCRIPTION = ""
    RATINGS = "div.rev div[class*='stars _s']"
    PRICE = "div.info div.prc"
    PRODUCT_LINK = "a.core"
    IMAGE_LINK = "div.img-c img.img"


def scrape_product_details(product_link):
    PL = ProductsLocator()
    PIL = ProductsInformationLocator()
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[502, 503, 504, 522, 524, 408, 429]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})

        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        price_elem = soup.select_one("div.df.-i-ctr.-fw-w")
        old_price_elem = price_elem.find("span", class_="-tal -gy5 -lthr -fs16 -pvxs -ubpt")
        old_price = old_price_elem.text.strip() if old_price_elem else None

        # Extract new price
        new_price_elem = price_elem.find("span", class_="-b -ubpt -tal -fs24 -prxs")
        new_price = new_price_elem.text.strip() if new_price_elem else None

        print("Old Price:", old_price)
        print("New Price:", new_price)

        name = soup.select_one("h1.-fs20.-pts.-pbxs")
        print(name.text)

        description = soup.select_one("div.card.aim.-mtm")
        print(description.text)

        images = soup.select("div.sldr._img._prod.-rad4.-oh.-mbs a")
        images_links = [img.get("href") for img in images]
        print(images_links)

        rating_div = soup.find("div", class_="-df -i-ctr -pbs")
        rating_text = rating_div.text.strip()
        print(rating_text)

    except Exception as e:
        print(f"Error occurred while scraping product details: {e}")
        return None


product ={"name": "kimani"}

print(product.na)