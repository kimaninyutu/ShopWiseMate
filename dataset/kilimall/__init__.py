import os
import time
import requests
from pymongo.server_api import ServerApi

import category_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

# Initialize webdriver (in this case, using Firefox)
driver = webdriver.Firefox()

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Kilimall"]
db = collection


# Function to scrape product information on the current page
def scrape_product_info():
    product_data = {}
    #product_info = []
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    for item in product_items:
        name = item.find_element(By.CLASS_NAME, "product-title").text
        product_link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        price = item.find_element(By.CLASS_NAME, "product-price").text
        rating = item.find_element(By.CLASS_NAME, "reviews").text
        image_link = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

        product_data = {
            "name": name,
            "link": product_link,
            "price": price,
            "rating": rating,
            "image": image_link
        }

        #product_info.append(product_data)
        print(f"Product Name: {name}")
        print(f"Product Link: {product_link}")
        print(f"Image Link: {image_link}")
        print("=" * 50)
    return product_data


def specific_product_info():
    product_description = driver.find_element(By.CLASS_NAME, "detail-card")
    product_images = driver.find_elements(By.CLASS_NAME, "thumbnails")
    for description, image in product_description, product_images:
        images = image.find_elements(By.CLASS_NAME, "img-item").get_attribute("data-src")
        other_images = description.find_elements(By.CSS_SELECTOR, "img").get_attribute("data-src")
        description = description.find_elements(By.CSS_SELECTOR, "div").get_attribute("p")
        specification = description.find_elements(By.CLASS_NAME, "specification-card").text

        product_data = {
            "Description": description,
            "Images": images,
            "OtherImages": other_images,
            "Specification": specification
        }


# Function to click the "Next" button
def click_next_button():
    next_button = driver.find_element(By.CSS_SELECTOR,
                                      ".van-pagination__item.van-pagination__item--next.van-hairline--surround")
    time.sleep(10)
    next_button.click()


# Main loop to navigate through pages and scrape data
for category_name, category_link in category_links.__dict__.items():
    if not category_name.startswith("__"):  # Skip any private attributes
        # Navigate to the category page
        driver.get(category_link)

        all_product_info = []
        for _ in range(300):  # Loop through all pages (adjust as needed)
            # Scrape product info on the current page
            current_page_products = scrape_product_info()
            db[category_name].insert_one(current_page_products)
            print(f"Scraped data from {category_name}, page {_ + 1}")
            # Click the "Next" button
            try:
                click_next_button()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
            except:
                print(f"No more pages available for {category_name}.")
                break

driver.quit()


#GET THE PRODUCT LINKS OPEN WEBDRIVER FOR EACH LINK AND scrape the other images ang description
def get_description():
    pass
