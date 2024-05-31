import time
from pymongo.server_api import ServerApi
import category_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.firefox.service import Service as FirefoxService

# Specify the path to geckodriver`
service = FirefoxService(executable_path='/usr/local/bin/geckodriver')
driver = webdriver.Firefox()

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Kil"]
db = collection


def scrape_product_info():
    product_data = []
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    for item in product_items:
        try:
            name = item.find_element(By.CLASS_NAME, "product-title").text
            product_link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            price = item.find_element(By.CLASS_NAME, "product-price").text
            rating = item.find_element(By.CLASS_NAME, "reviews").text
            image_link = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

            product_data.append({
                "name": name,
                "link": product_link,
                "price": price,
                "rating": rating,
                "image": image_link
            })

            print(f"Product Name: {name}")
            print(f"Product Link: {product_link}")
            print(f"Image Link: {image_link}")
            print("=" * 50)
        except Exception as e:
            print(f"Error while scraping product: {e}")
    return product_data

def click_next_button():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR,
                                          ".van-pagination__item.van-pagination__item--next.van-hairline--surround")
        time.sleep(10)
        next_button.click()
    except Exception as e:
        print(f"Error while clicking next button: {e}")


for category_name, category_link in category_links.__dict__.items():
    if not category_name.startswith("__"):  # Skip any private attributes
        driver.get(category_link)
        for _ in range(300):  # Loop through all pages (adjust as needed)
            current_page_products = scrape_product_info()
            if current_page_products:
                db[category_name].insert_many(current_page_products)
                print(f"Scraped data from {category_name}, page {_ + 1}")
            try:
                click_next_button()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
            except Exception as e:
                print(f"No more pages available for {category_name}: {e}")
                break

driver.quit()
connection.close()
