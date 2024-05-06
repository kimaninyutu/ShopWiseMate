import re
import requests
import os
from bs4 import BeautifulSoup
from categories_endpoints import Endpoint as EP, Endpoint
from products_locator import ProductsLocator as Locator
from products_information_locator import ProductsInformationLocator as PI
from n_pages import Number_of_pages

#pages_endpoint = f"?page={1}#catalog-listing"
MAIN_URL = f"https://www.jumia.co.ke/"
#JUMIA_PAGE = requests.get(MAIN_URL).content
#soup = BeautifulSoup(JUMIA_PAGE, "html.parser")

products_info = []  # Initialize an empty list to store product info


class GetDataFromJumia:

    @staticmethod
    def clean_filename(filename):
        # Remove invalid characters from the filename
        cleaned_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return cleaned_filename

    @staticmethod
    def get_phone_tablets():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "phoneTablets"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        #for product_info in products_info:
        #print(product_info)

    @staticmethod
    def get_electronics():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists
        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.ELECTRONICS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Electronics"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_appliances():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.APPLIANCES}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Appliances"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_health_beauty():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.HEALTH_BEAUTY}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Health_Beauty"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_fashion():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.FASHION}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Fashion"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_computing():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.COMPUTING}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Computing"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_supermarket():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.SUPERMARKET}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Supermarket"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_baby_products():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.BABY_PRODUCTS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "BabyProducts"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_sporting_goods():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.SPORTING_GOODS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "SportingGoods"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_automobile():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.AUTOMOBILE}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Automobile"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_gaming():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.GAMING}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Gaming"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_garden_outdoor():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.GARDEN_OUTDOOR}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "GardenOutdoor"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_books_movie_music():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.BOOKS_MOVIE_MUSIC}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "BooksMusicMovie"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_livestock():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.LIVESTOCK}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Livestock"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_industrial_scientific():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.INDUSTRIAL_SCIENTIFIC}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "IndustrialScientific"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_miscellaneous():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.MISCELLANEOUS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Miscellaneous"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_musical_instruments():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.MUSICAL_INSTRUMENTS}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "MusicalInstruments"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_pet_supplies():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.PET_SUPPLIES}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "PetSupplies"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_services():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.SERVICES}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "Services"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)

    @staticmethod
    def get_toys_games():
        os.makedirs("images", exist_ok=True)  # Ensure "images" folder exists

        for i in range(1, Number_of_pages + 1):
            pages_endpoint = f"?page={i}#catalog-listing"
            Page_url = f"{MAIN_URL}{EP.TOYS_GAMES}{pages_endpoint}"
            Content = requests.get(Page_url).content
            soup = BeautifulSoup(Content, "html.parser")
            Names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            Price = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            Ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            Product_Links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            Images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(Names, Price, Ratings, Product_Links, Images):
                product_name = name.text.strip()  # Remove leading/trailing whitespaces
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)  # Clean the product name
                image_url = image.get('data-src').split('?')[0]
                img_filename = f"{product_name_cleaned}.jpg"  # Construct the image filename
                category_folder = "ToysGames"  # Set the category folder name
                category_folder_path = os.path.join("images", category_folder)  # Construct the category folder path
                try:
                    os.makedirs(category_folder_path, exist_ok=True)  # Ensure the category folder exists
                    img_path = os.path.join(category_folder_path, img_filename)  # Construct the image path
                    with open(img_path, "wb") as file:
                        img_req = requests.get(image_url)
                        file.write(img_req.content)
                    # Append product info to products_info list
                    products_info.append({
                        "name": product_name,
                        "product_link": f"{MAIN_URL}{link['href']}",
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": img_path
                    })
                except Exception as e:
                    print(f"Error occurred while downloading image: {e}")

        # Print the collected product info outside of the loop
        # for product_info in products_info:
        # print(product_info)


run = GetDataFromJumia()
run.get_supermarket()
run.get_baby_products()
run.get_sporting_goods()
run.get_automobile()
run.get_gaming()
run.get_garden_outdoor()
run.get_books_movie_music()
run.get_livestock()
run.get_industrial_scientific()
run.get_miscellaneous()
run.get_musical_instruments()
run.get_pet_supplies()
run.get_services()

