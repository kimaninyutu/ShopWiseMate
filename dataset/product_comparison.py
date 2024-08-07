import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

cheapest_in_kilimal = []
cheapest_in_jumia = []
cheapest_of_all = []

def scrape_image_from_product_page(url):
    full_url = f"https://www.kilimall.co.ke/{url}"
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    image = soup.select_one('div.swipe-image img')['src']
    return image

class KilimallScraper:
    def __init__(self, driver):
        self.driver = driver

    def search(self, product_name):
        self.driver.get("https://www.kilimall.co.ke/")
        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input.van-field__control')
        search_bar.clear()
        search_bar.send_keys(product_name)
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'div.search-button')
        search_button.click()
        time.sleep(5)

    def get_search_results(self, product_name):
        def contains_all_keywords(product_name, keywords):
            return all(keyword.lower() in product_name.lower() for keyword in keywords)

        keywords = product_name.split()
        products = []
        search_results = self.driver.find_elements(By.CSS_SELECTOR, 'div.listing-item')
        for product in search_results:
            try:
                name = product.find_element(By.CSS_SELECTOR, 'p.product-title').text
                if not contains_all_keywords(name, keywords):
                    continue

                price = product.find_element(By.CSS_SELECTOR, 'div.product-price').text
                link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                image = product.find_element(By.CSS_SELECTOR, 'div.product-image img').get_attribute('src')

                if not image:
                    image = scrape_image_from_product_page(link)

                rating = len(product.find_elements(By.CSS_SELECTOR, 'div.van-rate i.van-rate__icon--full'))
                price = float(price.replace("KSh ", "").replace(",", ""))
                products.append({"name": name, "price": price, "link": link, "image": image, "rating": rating})
            except Exception as e:
                print(f"Error extracting product details from Kilimall: {e}")
        return products

    def close(self):
        self.driver.quit()

class JumiaScraper:
    def __init__(self, driver):
        self.driver = driver

    def search(self, product_name):
        self.driver.get("https://www.jumia.co.ke/")
        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        search_bar.clear()
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)

    def get_search_results(self):
        products = []
        search_results = self.driver.find_elements(By.CSS_SELECTOR, 'article[class*="prd _fb col c-prd"]')
        for product in search_results:
            try:
                name = product.find_element(By.CSS_SELECTOR, 'h3[class*="name"]').text
                price = product.find_element(By.CSS_SELECTOR, 'div[class*="prc"]').text
                old_price = product.find_elements(By.CSS_SELECTOR, 'div[class*="old"]')
                old_price = old_price[0].text if old_price else None
                link = product.find_element(By.CSS_SELECTOR, 'a.core').get_attribute('href')
                image = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

                if image.startswith("data:image"):
                    image = None

                rating = product.find_elements(By.CSS_SELECTOR, 'div[class*="bdg _glb _xs"]')
                rating = rating[0].text if rating else "No rating"

                price = float(price.replace("KSh ", "").replace(",", ""))

                products.append({"name": name, "price": price, "old_price": old_price, "link": link, "image": image,
                                 "rating": rating})
            except Exception as e:
                print(f"Error extracting product details from Jumia: {e}")
        return products

    def close(self):
        self.driver.quit()

def compare_prices(product_name):
    chrome_kilimall = webdriver.Chrome()
    scraper_kilimall = KilimallScraper(chrome_kilimall)

    chrome_jumia = webdriver.Chrome()
    scraper_jumia = JumiaScraper(chrome_jumia)

    try:
        scraper_kilimall.search(product_name)
        results_kilimall = scraper_kilimall.get_search_results(product_name)

        if not results_kilimall:
            print("No products found on Kilimall.")
            return

        prices_kilimall = [product['price'] for product in results_kilimall]
        cheapest_price_kilimall = min(prices_kilimall)
        cheapest_product_kilimall = results_kilimall[prices_kilimall.index(cheapest_price_kilimall)]
        cheapest_in_kilimal.append(cheapest_product_kilimall)

        time.sleep(2)
        scraper_jumia.search(product_name)
        results_jumia = scraper_jumia.get_search_results()

        if not results_jumia:
            print("No products found on Jumia.")
            return

        prices_jumia = [product['price'] for product in results_jumia]
        cheapest_price_jumia = min(prices_jumia)
        cheapest_product_jumia = results_jumia[prices_jumia.index(cheapest_price_jumia)]

        cheapest_in_jumia.append(cheapest_product_jumia)

        if cheapest_price_jumia < cheapest_price_kilimall:
            cheapest_of_all.append(cheapest_product_jumia)
            return cheapest_product_jumia
        else:
            cheapest_of_all.append(cheapest_product_kilimall)
            return cheapest_product_kilimall

    except Exception as e:
        print(f"An error occurred while comparing prices: {e}")

    finally:
        scraper_jumia.close()
        scraper_kilimall.close()

class Compare:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def clean_product_name(name):
        return re.sub(r'\s*\([^)]*\)', '', name).strip()

    @staticmethod
    def compare(name):
        cleaned_name = Compare.clean_product_name(name)
        compare_prices(cleaned_name)
