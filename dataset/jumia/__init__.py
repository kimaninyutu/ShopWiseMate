import re
import requests
import os
from bs4 import BeautifulSoup
from pymongo.server_api import ServerApi

from categories_endpoints import Endpoint as EP, Endpoint
from products_locator import ProductsLocator as Locator
from products_information_locator import ProductsInformationLocator as PI
from n_pages import Number_of_pages
from pymongo import MongoClient

#pages_endpoint = f"?page={1}#catalog-listing"
MAIN_URL = f"https://www.jumia.co.ke/"
#JUMIA_PAGE = requests.get(MAIN_URL).content
#soup = BeautifulSoup(JUMIA_PAGE, "html.parser")

products_info = []  # Initialize an empty list to store product info
uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Jumia"]
db = collection


class GetDataFromJumia:

    @staticmethod
    def clean_filename(filename):
        # Remove invalid characters from the filename
        cleaned_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return cleaned_filename

    @staticmethod
    def get_phone_tablets():
        for i in range(1, Number_of_pages+1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "phoneTablets"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    #products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")


    @staticmethod
    def get_electronics():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "electronics"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_appliances():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "appliances"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_health_beauty():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "health_beauty"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_fashion():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "fashion"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_computing():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "computing"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_supermarket():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "supermarket"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_baby_products():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "baby_products"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_sporting_goods():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "sporting_goods"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_automobile():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "automobile"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_gaming():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "gaming"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_garden_outdoor():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "garden_outdoor"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_books_movie_music():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "books_movie_music"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_livestock():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "livestock"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")
    @staticmethod
    def get_industrial_scientific():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "industrial_scientific"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_miscellaneous():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "miscellaneous"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_musical_instruments():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "musical_instruments"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_pet_supplies():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "pet_supplies"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_services():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "services"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

    @staticmethod
    def get_toys_games():
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                category = "toys_games"
                product_link = f"{MAIN_URL}{link['href']}"
                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scrapping {product_name} from jumia")
                    products_soup = BeautifulSoup(requests.get(product_link).content, "html.parser")
                    product_data = products_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img")

                    for data in product_data:
                        if data.name == "img":
                            images_urls.append(data['data-src'])
                        else:
                            product_descriptions.append(data.text)

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "images_link": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)  # Insert product data into MongoDB
                    # products_info.append(product_data)
                    print(f"Scrapped {product_name} from jumia")
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")


run = GetDataFromJumia()
run.get_phone_tablets()
