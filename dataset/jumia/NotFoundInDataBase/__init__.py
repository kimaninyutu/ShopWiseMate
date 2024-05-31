import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from urllib3 import Retry

from Page_Locators import Page_Locators
from products_locators import ProductsLocators

MAIN_URI = "https://www.jumia.co.ke/"

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Jumia"]
db = collection["NotFoundInDataBase"]


class SearchProduct:
    def __init__(self, driver):
        self.driver = driver

    def search(self, product_name):
        self.driver.get(MAIN_URI)
        search_bar = self.driver.find_element(By.CSS_SELECTOR, Page_Locators.SEARCH_BAR)
        search_bar.clear()
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)  # Press enter to submit the search
        time.sleep(5)  # Wait for the results to load

    def get_search_results(self):
        products = []
        search_results = self.driver.find_elements(By.CSS_SELECTOR, ProductsLocators.PRODUCT_LOCATOR)
        for product in search_results:
            try:
                name = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_NAME).text
                price = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_PRICE).text
                old_price_elements = product.find_elements(By.CSS_SELECTOR, ProductsLocators.PRODUCT_OLD_PRICE)
                old_price = old_price_elements[0].text if old_price_elements else None
                link = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_LINK).get_attribute('href')
                image = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_IMAGE).get_attribute('src')
                rating_elements = product.find_elements(By.CSS_SELECTOR, ProductsLocators.PRODUCT_RATING)
                rating = rating_elements[0].text if rating_elements else "No rating"

                products.append({
                    "name": name,
                    "price": price,
                    "old_price": old_price,
                    "link": link,
                    "image": image,
                    "rating": rating
                })
            except Exception as e:
                print(f"Error extracting product details: {e}")
        return products

    def close(self):
        self.driver.quit()


# Example usage
if __name__ == "__main__":
    chrome = webdriver.Chrome()
    search_product = SearchProduct(chrome)
    search_product.search("laptop")  # -------------------<< Change to respective search name
    results = search_product.get_search_results()
    for result in results:
        link = result.get("link")
        name = result.get("name")
        price = result.get("price")
        rating = result.get("rating")
        images_urls = []
        product_descriptions = []
        ratings = []
        product_content = requests.get(link).content
        soup = BeautifulSoup(product_content, "html.parser")

        product_img = soup.select("section.col12.-df.-d-co")
        for tag in product_img:
            image = tag.select_one("img")
            images_urls.append(image.get("data-src"))

        product_description = soup.select("div.markup.-mhm.-pvl.-oxa.-sc")
        for p in product_description:
            description = p.text
            product_descriptions.append(description)

        product_info = {"name": name, "price": price, "images": images_urls, "description": product_descriptions,
                        "rating": ratings, "link": link}
        db.insert_one(product_info)
    search_product.close()
