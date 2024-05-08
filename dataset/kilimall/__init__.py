import os
import time
import requests
import category_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize webdriver (in this case, using Firefox)
driver = webdriver.Firefox()


# Function to scrape product information on the current page
def scrape_product_info():
    product_info = []
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    for item in product_items:
        name = item.find_element(By.CLASS_NAME, "product-title").text
        product_link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        price = item.find_element(By.CLASS_NAME, "product-price").text
        rating = item.find_element(By.CLASS_NAME, "reviews").text
        image_link = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        product_info.append(
            {"Name": name, "Price": price, "Rating": rating, "ImageLink": image_link, "ProductLink": product_link})
        print(f"Product Name: {name}")
        print(f"Price: {price}")
        print(f"Rating: {rating}")
        print(f"Product Link: {product_link}")
        print(f"Image Link: {image_link}")
        print("=" * 50)
    return product_info


# Function to click the "Next" button
def click_next_button():
    next_button = driver.find_element(By.CSS_SELECTOR,
                                      ".van-pagination__item.van-pagination__item--next.van-hairline--surround")
    time.sleep(10)
    next_button.click()


# Function to download and save image
def download_image(image_url, filename):
    try:
        response = requests.get(image_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading image: {e}")


# Main loop to navigate through pages and scrape data
for category_name, category_link in category_links.__dict__.items():
    if not category_name.startswith("__"):  # Skip any private attributes
        # Navigate to the category page
        driver.get(category_link)

        # Create a subfolder for the category if it doesn't exist
        category_folder = os.path.join("images", category_name)
        os.makedirs(category_folder, exist_ok=True)

        all_product_info = []
        for _ in range(300):  # Loop through all pages (adjust as needed)
            # Scrape product info on the current page
            current_page_products = scrape_product_info()
            all_product_info.extend(current_page_products)
            print(f"Scraped data from {category_name}, page {_ + 1}")

            # Download images
            for product in current_page_products:
                image_url = product['ImageLink']
                if image_url:
                    image_name = product['Name'].replace("/", "_").replace(":", "") + ".jpg"
                    image_path = os.path.join(category_folder, image_name)
                    download_image(image_url, image_path)

            # Click the "Next" button
            try:
                click_next_button()
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
            except:
                print(f"No more pages available for {category_name}.")
                break


driver.quit()
