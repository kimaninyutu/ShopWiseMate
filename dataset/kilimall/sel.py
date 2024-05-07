import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize webdriver (in this case, using Firefox)
driver = webdriver.Firefox()

# Navigate to the initial page
driver.get("https://www.kilimall.co.ke/search-result?id=968&form=category&ctgName=Shoes")


# Function to scrape product information on the current page
def scrape_product_info():
    product_info = []
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    for item in product_items:
        name = item.find_element(By.CLASS_NAME, "product-title").text
        price = item.find_element(By.CLASS_NAME, "product-price").text
        rating = item.find_element(By.CLASS_NAME, "reviews").text
        product_info.append({"Name": name, "Price": price, "Rating": rating})
    return product_info


# Function to click the "Next" button
def click_next_button():
    next_button = driver.find_element(By.CSS_SELECTOR,
                                      ".van-pagination__item.van-pagination__item--next.van-hairline--surround")
    next_button.click()


# Main loop to navigate through pages and scrape data
all_product_info = []
for _ in range(278):  # Loop through all 278 pages
    # Scrape product info on the current page
    current_page_products = scrape_product_info()
    all_product_info.extend(current_page_products)
    print(f"Scraped data from page {_ + 1}")

    # Click the "Next" button
    try:
        click_next_button()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))
        time.sleep(5)
    except:
        print("No more pages available.")
        break

# Print the scraped product info
for product in all_product_info:
    print(product)

# Close the webdriver
driver.quit()
