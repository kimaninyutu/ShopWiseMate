import category_links
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
from pymongo.server_api import ServerApi


#driver = webdriver.Firefox()


uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Kilimall"]
db = collection


# Function to scrape product information on the current page
class EachProduct:

    @staticmethod
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

        return product_data

    @staticmethod
    def get_category():
        for categoryname, categorylink in category_links.__dict__.items():
            database_categories = db[categoryname]
            #data = {"categoryname": categoryname}
            print(database_categories)
            print(db )


ST = EachProduct()
ST.get_category()

