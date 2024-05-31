import category_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import time

# Define MongoDB connection URI
uri = ("mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
db = connection["Kilimall"]

# Function to scrape product information on the current page
class EachProduct:

    def __init__(self, driver):
        self.driver = driver

    def specific_product_info(self, product_url):
        self.driver.get(product_url)
        time.sleep(3)  # Adjust sleep time as necessary
        product_data = {}

        try:
            product_description = self.driver.find_element(By.CLASS_NAME, "detail-card").text
            product_images = self.driver.find_elements(By.CLASS_NAME, "img-item")
            images = [image.get_attribute("data-src") for image in product_images]

            old_price = self.driver.find_element(By.CLASS_NAME, "old-price").text
            new_price = self.driver.find_element(By.CLASS_NAME, "new-price").text
            product_name = self.driver.find_element(By.CLASS_NAME, "product-title").text
            specifications = self.driver.find_element(By.CLASS_NAME, "specification-card").text

            product_data = {
                "Name": product_name,
                "Description": product_description,
                "Images": images,
                "Old Price": old_price,
                "New Price": new_price,
                "Specifications": specifications
            }
        except Exception as e:
            print(f"Error extracting product details: {e}")

        return product_data

    def get_category(self):
        for category_name, category_link in category_links.__dict__.items():
            if not category_name.startswith('__'):
                database_category = db[category_name]
                print(f"Scraping category: {category_name}")

                self.driver.get(category_link)
                time.sleep(5)  # Adjust sleep time as necessary
                product_links = self.driver.find_elements(By.CSS_SELECTOR, "a.product-link")

                for product_link in product_links:
                    product_url = product_link.get_attribute('href')
                    product_data = self.specific_product_info(product_url)
                    database_category.insert_one(product_data)
                    print(f"Inserted product: {product_data['Name']}")

# Main execution
if __name__ == "__main__":
    driver = webdriver.Chrome()
    scraper = EachProduct(driver)
    scraper.get_category()
    driver.quit()
