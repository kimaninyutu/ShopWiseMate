import os
import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from dotenv import load_dotenv

from kilimall_locators import PageLocators, ProductsLocators

load_dotenv()  # Load environment variables from .env file

MAIN_URI = "https://www.kilimall.co.ke/"
MONGO_URI = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority"
             "&appName"
             "=Cluster0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new client and connect to the server
connection = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = connection["Kilimall"]["NotFoundInDataBase"]


class SearchProduct:
    def __init__(self, driver):
        self.driver = driver

    def search(self, product_name):
        try:
            self.driver.get(MAIN_URI)
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, PageLocators.SEARCH_BAR))
            )
            search_bar.clear()
            search_bar.send_keys(product_name)
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, PageLocators.SEARCH_BUTTON))
            )
            search_button.click()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error during search: {e}")

    def get_search_results(self):
        products = []
        try:
            search_results = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ProductsLocators.PRODUCT_CONTAINER))
            )
            
            for product in search_results:

                try:
                    name = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_NAME).text
                    price = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_PRICE).text
                    link = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_LINK).get_attribute('href')
                    image = product.find_element(By.CSS_SELECTOR, ProductsLocators.PRODUCT_IMAGE).get_attribute('src')
                    rating = len(product.find_elements(By.CSS_SELECTOR,
                                                       ProductsLocators.PRODUCT_RATING + ' i.van-rate__icon--full'))

                    print(name)
                    print(link)
                    print(rating)

                    products.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "image": image,
                        "rating": rating,
                    })

                except Exception as e:
                    logger.error(f"Error extracting product details: {e}")
        except Exception as e:
            logger.error(f"Error getting search results: {e}")
        return products

    def close(self):
        self.driver.quit()


def scrape_product_details(link):
    try:
        product_content = requests.get(link).content
        soup = BeautifulSoup(product_content, "html.parser")
        images_urls = [img.get("data-src") for img in soup.select("div.product-images img")]
        product_descriptions = [desc.text for desc in soup.select("div.product-description p")]
        return images_urls, product_descriptions
    except Exception as e:
        logger.error(f"Error scraping product details from {link}: {e}")
        return [], []


def main():
    try:
        chrome = webdriver.Chrome()
        search_product = SearchProduct(chrome)
        search_product.search("laptop")  # Change the search term as needed
        results = search_product.get_search_results()
        for result in results:
            link = result.get("link")
            name = result.get("name")
            price = result.get("price")
            rating = result.get("rating")
            images_urls, product_descriptions = scrape_product_details(link)

            product_info = {
                "name": name,
                "price": price,
                "images": images_urls,
                "description": product_descriptions,
                "rating": rating,
                "link": link
            }
            db.insert_one(product_info)
        search_product.close()
    except Exception as e:
        logger.error(f"Error in main function: {e}")


if __name__ == "__main__":
    main()
