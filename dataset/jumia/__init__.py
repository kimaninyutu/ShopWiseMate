import re
import time
import requests
from bs4 import BeautifulSoup
from pymongo.server_api import ServerApi
from categories_endpoints import Endpoint as EP
from products_locator import ProductsLocator as Locator
from products_information_locator import ProductsInformationLocator as PI
from n_pages import Number_of_pages  # Ensure this is correctly defined and imported
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

#pages_endpoint = f"?page={1}#catalog-listing"
MAIN_URL = f"https://www.jumia.co.ke/"
#JUMIA_PAGE = requests.get(MAIN_URL).content
#soup = BeautifulSoup(JUMIA_PAGE, "html.parser")

products_info = []  # Initialize an empty list to store product info
uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
connection = MongoClient(uri, server_api=ServerApi('1'))
collection = connection["Jumia"]
db = collection


class GetDataFromJumia:

    @staticmethod
    def clean_filename(filename):
        # Remove invalid characters from the filename
        cleaned_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return cleaned_filename

    @staticmethod
    def get_phone_tablets():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.PHONE_TABLETS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "phoneTablets"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_electronics():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.ELECTRONICS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "electronics"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_appliances():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.APPLIANCES}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "appliances"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_health_beauty():
        for i in range(36, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.HEALTH_BEAUTY}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "health_beauty"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_computing():
        for i in range(36, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.COMPUTING}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "computing"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_supermarket():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.SUPERMARKET}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "supermarket"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_baby_products():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.BABY_PRODUCTS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "babyproducts"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_sporting_goods():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.SPORTING_GOODS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "sportinggoods"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_automobile():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.AUTOMOBILE}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "automobile"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_gaming():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.GAMING}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "gaming"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_garden_outdoor():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.GARDEN_OUTDOOR}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "gardenoutdoor"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_books_movie_music():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.BOOKS_MOVIE_MUSIC}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "books_movie_music"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_livestock():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.LIVESTOCK}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "livestock"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_industrial_scientific():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.INDUSTRIAL_SCIENTIFIC}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "industrialscientific"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")
    @staticmethod
    def get_miscellaneous():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.MISCELLANEOUS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "miscellaneous"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_musical_instruments():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.MUSICAL_INSTRUMENTS}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "musicalintruments"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_pet_supplies():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.PET_SUPPLIES}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "petsupplies"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_services():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.SERVICES}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "services"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")

    @staticmethod
    def get_toys_games():
        for i in range(1, Number_of_pages + 10):
            pages_endpoint = f"?page={i}#catalog-listing"
            page_url = f"{MAIN_URL}{EP.TOYS_GAMES}{pages_endpoint}"

            # Adding retry logic
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504, 522, 524, 408, 429]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()  # Raise HTTPError for bad responses
                content = response.content
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                continue

            soup = BeautifulSoup(content, "html.parser")
            names = soup.select(f"{Locator.LOCATOR} {PI.NAME}")
            prices = soup.select(f"{Locator.LOCATOR} {PI.PRICE}")
            ratings = soup.select(f"{Locator.LOCATOR} {PI.RATINGS}")
            product_links = soup.select(f"{Locator.LOCATOR} {PI.PRODUCT_LINK}")
            images = soup.select(f"{Locator.LOCATOR} {PI.IMAGE_LINK}")

            for name, price, rating, link, image in zip(names, prices, ratings, product_links, images):
                product_name = name.text.strip()
                product_name_cleaned = GetDataFromJumia.clean_filename(product_name)
                image_url = image.get('data-src').split('?')[0] if image.get('data-src') else image.get('src')
                category = "toy_games"
                product_link = f"{MAIN_URL}{link['href']}"

                try:
                    images_urls = [image_url]
                    product_descriptions = []
                    print(f"Scraping {product_name} from Jumia")
                    product_response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    product_data_elements = product_soup.select(
                        "div[class*='markup -mhm -pvl -oxa -sc'] li, div[class*='markup -mhm -pvl -oxa -sc'] ul,"
                        "div[class*='markup -mhm -pvl -oxa -sc'] img, div[class*='markup -mhm -pvl -oxa -sc'] p, "
                        "div[class*='markup -mhm -pvl -oxa -sc']"
                    )

                    for data in product_data_elements:
                        if data.name == "img":
                            image_source = data.get('data-src') or data.get('src')
                            if image_source:
                                images_urls.append(image_source)
                        elif data.name == "a":
                            images_urls.append(data.get('href'))
                        else:
                            product_descriptions.append(data.text.strip())

                    product_data = {
                        "name": product_name,
                        "product_link": product_link,
                        "price": price.text.strip(),
                        "rating": rating.text.strip(),
                        "image": image_url,
                        "other_images": images_urls,
                        "product_descriptions": product_descriptions
                    }
                    db[category].insert_one(product_data)
                    print(f"Scraped {product_name} from Jumia")
                except Exception as e:
                    print(f"Error occurred while processing product {product_name}: {e}")
            print(f"Finished page {i}")


run = GetDataFromJumia()
#run.get_phone_tablets()
#run.get_electronics()
#run.get_appliances()
#run.get_health_beauty()

run.get_computing()
print(f"Finished scrapping THe Category computing")
for i in range(20):
    print(f"--------------"*25)
run.get_supermarket()
print(f"Finished scrapping THe Category supermarket")
for i in range(20):
    print(f"--------------"*25)
run.get_baby_products()
print(f"Finished scrapping THe Category babyproducts")
for i in range(20):
    print(f"--------------"*25)
run.get_sporting_goods()
print(f"Finished scrapping THe Category spoting goods")
for i in range(20):
    print(f"--------------"*25)
run.get_automobile()
print(f"Finished scrapping THe Category automobile")
for i in range(20):
    print(f"--------------"*25)
run.get_gaming()
print(f"Finished scrapping THe Category gaming")
for i in range(20):
    print(f"--------------"*25)
run.get_garden_outdoor()
print(f"Finished scrapping THe Category garden outdoor")
for i in range(20):
    print(f"--------------"*25)
run.get_books_movie_music()
print(f"Finished scrapping THe Category books movie music")
for i in range(20):
    print(f"--------------"*25)
run.get_livestock()
print(f"Finished scrapping THe Category liverstock")
for i in range(20):
    print(f"--------------"*25)
run.get_industrial_scientific()
print(f"Finished scrapping THe Category industrial scientific")
for i in range(20):
    print(f"--------------"*25)
run.get_miscellaneous()
print(f"Finished scrapping THe Category misceoues")
for i in range(20):
    print(f"--------------"*25)
run.get_musical_instruments()
print(f"Finished scrapping THe Category musical inbtruments")
for i in range(20):
    print(f"--------------"*25)
run.get_pet_supplies()
print(f"Finished scrapping THe Category supplies")
for i in range(20):
    print(f"--------------"*25)
run.get_services()
print(f"Finished scrapping THe Category services")
for i in range(20):
    print(f"--------------"*25)
run.get_toys_games()
print(f"Finished scrapping THe Category toys and games")
for i in range(20):
    print(f"--------------"*25)
