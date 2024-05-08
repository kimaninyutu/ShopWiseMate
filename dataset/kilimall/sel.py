import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize webdriver (in this case, using Firefox)
driver = webdriver.Firefox()

# Navigate to the initial page
driver.get("https://www.kilimall.co.ke/search-result?id=968&form=category&ctgName=Shoes")

# Create the 'images' directory if it doesn't exist
os.makedirs("images", exist_ok=True)


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
        product_info.append({"Name": name, "Price": price, "Rating": rating, "ImageLink": image_link, "ProductLink": product_link})
    return product_info


# Function to click the "Next" button
def click_next_button():
    next_button = driver.find_element(By.CSS_SELECTOR,
                                      ".van-pagination__item.van-pagination__item--next.van-hairline--surround")
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
all_product_info = []
for _ in range(1):  # Loop through all 278 pages
    # Scrape product info on the current page
    current_page_products = scrape_product_info()
    all_product_info.extend(current_page_products)
    print(f"Scraped data from page {_ + 1}")

    # Download images
    for product in current_page_products:
        image_url = product['ImageLink']
        if image_url:
            image_name = product['Name'].replace("/", "_").replace(":", "") + ".jpg"
            image_path = os.path.join("images", image_name)
            download_image(image_url, image_path)

    # Click the "Next" button
    try:
        click_next_button()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
        time.sleep(5)
    except:
        print("No more pages available.")
        break

# Print the scraped product info
for product in all_product_info:
    print(product)

# Close the webdriver
driver.quit()
