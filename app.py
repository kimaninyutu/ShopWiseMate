import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bson.objectid import ObjectId  # Ensure this import for ObjectId
from dataset.product_comparison import Compare, cheapest_in_kilimal, cheapest_in_jumia, cheapest_of_all
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

# Configure the Flask app before creating the SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tjisisasecretkey'

config_class = 'config.DevelopmentConfig' if os.getenv('FLASK_ENV') == 'development' else 'config.ProductionConfig'
app.config.from_object(config_class)

# Initialize the SQLAlchemy instance after the configuration
db = SQLAlchemy(app)

# MongoDB connection for Jumia
uri_jumia = (
    "mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
    "=Cluster0")
client_jumia = MongoClient(uri_jumia, server_api=ServerApi('1'))
database_jumia = client_jumia["Jumia"]
collection_names_jumia = database_jumia.list_collection_names()


# MongoDB connection for Kil
uri_kil = (
    "mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client_kil = MongoClient(uri_kil, server_api=ServerApi('1'))
database_kil = client_kil["Kil"]
collection_names_kil = database_kil.list_collection_names()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), unique=True, nullable=False)


def get_products(database, collection_name, limit=500):
    products = []
    collection = database[collection_name]
    print(f"Retrieving documents from collection: {collection_name}")

    documents = collection.find({}, {
        "name": 1,
        "product_link": 1,
        "price": 1,
        "rating": 1,
        "image": 1,
        "other_images": 1,
        "product_descriptions": 1
    }).limit(limit)

    for document in documents:
        products.append(document)

    return products


valid_collections = {
    "phoneTablets": "PHONE_TABLETS",
    "electronics": "ELECTRONICS",
    "appliances": "APPLIANCES",
    "health-beauty": "HEALTH_BEAUTY",
    "home-office": "HOME_OFFICE",
    "fashion": "FASHION",
    "computing": "COMPUTING",
    "supermarket": "SUPERMARKET",
    "babyproducts": "BABY_PRODUCTS",
    "sportinggoods": "sporting-goods",
    "automobile": "AUTOMOBILE",
    "gaming": "GAMING",
    "gardenoutdoor": "GARDEN_OUTDOOR",
    "books_movie_music": "BOOKS_MOVIE_MUSIC",
    "livestock": "LIVESTOCK",
    "industrialscientific": "INDUSTRIAL_SCIENTIFIC",
    "miscellaneous": "MISCELLANEOUS",
    "musicalintruments": "MUSICAL_INSTRUMENTS",
    "petsupplies": "PET_SUPPLIES",
    "services": "SERVICES",
    "toys_games": "TOYS_GAMES",
    "other": "OTHER"
}


def search_products(search_term):
    products = []

    # Search in Jumia collections
    for collection_name in collection_names_jumia:
        collection = database_jumia[collection_name]
        documents = collection.find({"name": {"$regex": search_term, "$options": "i"}}, {
            "name": 1,
            "product_link": 1,
            "price": 1,
            "rating": 1,
            "image": 1,
            "other_images": 1,
            "product_descriptions": 1
        })
        for document in documents:
            document['source'] = 'Jumia'
            products.append(document)

    # Search in Kil collections
    for collection_name in collection_names_kil:
        collection = database_kil[collection_name]
        documents = collection.find({"name": {"$regex": search_term, "$options": "i"}}, {
            "name": 1,
            "product_link": 1,
            "price": 1,
            "rating": 1,
            "image": 1,
            "other_images": 1,
            "product_descriptions": 1
        })
        for document in documents:
            document['source'] = 'Kil'
            products.append(document)

    return products


def get_product_by_id(database, product_id):
    for collection_name in database.list_collection_names():
        collection = database[collection_name]
        product = collection.find_one({"_id": ObjectId(product_id)})  # Ensure ObjectId is used
        if product:
            return product
    return None


def get_related_products(category, source='Jumia', limit=5):
    related_products = []

    if source == 'Jumia':
        database = database_jumia
        collection_names = collection_names_jumia
    else:
        database = database_kil
        collection_names = collection_names_kil

    collection_name = valid_collections.get(category)
    if collection_name in collection_names:
        related_products = get_products(database, collection_name, limit)
    return related_products


def scrape_product_details(product_link):
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
        response = session.get(product_link, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        price_container = soup.select_one("div.df.-i-ctr.-fw-w")
        if not price_container:
            raise ValueError("Price container not found")

        new_price_elem = price_container.select_one("span.-b.-ubpt.-tal.-fs24.-prxs")
        new_price = new_price_elem.text.strip() if new_price_elem else None

        old_price_elem = price_container.select_one("span.-tal.-gy5.-lthr.-fs16.-pvxs.-ubpt")
        old_price = old_price_elem.text.strip() if old_price_elem else None

        name_elem = soup.select_one("h1.-fs20.-pts.-pbxs")
        if not name_elem:
            raise ValueError("Name element not found")
        name = name_elem.text.strip()

        description_elem = soup.select_one("div.card.aim.-mtm")
        description = description_elem.text.strip().replace('\r', '').replace('\n', '\n') if description_elem else "N/A"

        images = soup.select("div.sldr._img._prod.-rad4.-oh.-mbs a")
        image = [img.get("href") for img in images]

        rating_elem = soup.find("div", class_="-df -i-ctr -pbs")
        rating = rating_elem.text.strip() if rating_elem else "N/A"

        product_data = {
            "name": name,
            "product_link": product_link,
            "price": new_price if new_price else "N/A",
            "old_price": old_price,
            "rating": rating,
            "image": image[0] if image else None,
            "other_images": [img.get("href") for img in images],
            "description": description
        }
        return product_data

    except Exception as e:
        print(f"Error occurred while scraping product details: {e}")
        return None


def scrape_product_from_kilimall(link):
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
        response = session.get(link, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        price_elem = soup.select_one("div.product-price")
        old_price_elem = price_elem.find("span", class_="del-price")
        old_price = old_price_elem.text.strip() if old_price_elem else None

        new_price_elem = price_elem.find("span", class_="sale-price")
        new_price = new_price_elem.text.strip() if new_price_elem else None

        name_elem = soup.select_one("div.product-title")
        description_elem = soup.select_one("div.specification-card")
        images = soup.select("div.details")
        image = [img.get("src") for img in images]

        rating_elem = soup.find("div", class_="van-rate")

        name = name_elem.text.strip() if name_elem else "N/A"
        price = new_price if new_price else "N/A"
        old_price = old_price if old_price else None
        rating = rating_elem.text.strip() if rating_elem else "N/A"

        description = description_elem.text.strip().replace('\r', '').replace('\n', '\n') if description_elem else "N/A"

        images_urls = [img.get("src") for img in images]
        print(images_urls)
        product_data = {
            "name": name,
            "product_link": link,
            "price": price,
            "old_price": old_price,  # Add the old price here
            "rating": rating,
            "image": image[0] if image else None,
            "other_images": images_urls,
            "description": description
        }
        return product_data

    except Exception as e:
        print(f"Error occurred while scraping product details: {e}")
        return None


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        search = request.args.get("searchProduct")
        if search:
            print(search)
            search_results = search_products(search)
            return render_template("search_results.html", products=search_results, search_term=search)
        else:
            pass
    return render_template("home.html")


@app.route("/<category>", methods=["GET", "POST"])
def show_category(category):
    if category not in valid_collections:
        return "Category not found", 404

    collection_name = valid_collections[category]

    jumia_instance = get_products(database_jumia, category)
    products = jumia_instance
    print(products)

    return render_template("category.html", category=category.replace("-", " ").title(), products=products)


@app.route("/product/<product_id>", methods=["GET", "POST"])
def product_page(product_id):
    product = get_product_by_id(database_jumia, product_id) or get_product_by_id(database_kil, product_id)
    if not product:
        return "Product not found", 404

    detailed_product = scrape_product_details(product['product_link'])
    if not detailed_product:
        return "Could not retrieve product details", 500

    related_products = get_related_products(product.get("category", ""))

    if request.method == "POST":
        if 'find_cheapest' in request.form:
            product_name = request.form.get("name")
            compare = Compare(product_name)
            compare.compare(product_name)

            # Ensure the lists are not empty
            if cheapest_in_jumia:
                product1 = cheapest_in_jumia[0]
                jumia = scrape_product_details(product1["link"])
            else:
                jumia = None

            if cheapest_in_kilimal:
                product2 = cheapest_in_kilimal[0]
                kilimal = scrape_product_from_kilimall(product2["link"])
            else:
                kilimal = None

            if cheapest_of_all:
                product3 = cheapest_of_all[0]
                if cheapest_of_all is cheapest_in_jumia:
                    cheapest = jumia
                elif cheapest_of_all is cheapest_in_kilimal:
                    cheapest = kilimal
                else:
                    cheapest = None
            else:
                cheapest = None

            return render_template(
                "compare.html",
                product1=jumia,
                product2=kilimal,
                product3=cheapest
            )
        else:
            # Handle add to cart or view product form submission here
            pass

    return render_template("product_page.html", product=detailed_product, related_products=related_products)


@app.route("/jumia")
def show_jumia():
    return render_template("home.html")


@app.route("/kilimall")
def show_kilimall():
    return render_template("home.html")



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
