import functools
import os
import secrets
import datetime

import bson
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bson.objectid import ObjectId
from dataset.product_comparison import Compare, cheapest_in_kilimal, cheapest_in_jumia, cheapest_of_all
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(32)
config_class = 'config.DevelopmentConfig' if os.getenv('FLASK_ENV') == 'development' else 'config.ProductionConfig'
app.config.from_object(config_class)

users_uri = (
    "mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
    "=Cluster0")

users_db = MongoClient(users_uri, server_api=ServerApi("1"))
users_database = users_db["users"]
users_collection = users_database["users"]

# MongoDB connection for Jumia
uri_jumia = (
    "mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
    "=Cluster0")
client_jumia = MongoClient(uri_jumia, server_api=ServerApi('1'))
database_jumia = client_jumia["Jumia"]
collection_names_jumia = database_jumia.list_collection_names()

# MongoDB connection for Kil
uri_kil = (
    "mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
    "=Cluster0")
client_kil = MongoClient(uri_kil, server_api=ServerApi('1'))
database_kil = client_kil["Kil"]
collection_names_kil = database_kil.list_collection_names()


def login_required(route):
    @functools.wraps(route)
    def wrapped_route(*args, **kwargs):
        email = session.get('email')
        if not email or not users_collection.find_one({"email": email}):
            return redirect(url_for("login"))
        return route(*args, **kwargs)

    return wrapped_route


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
    "computing": "COMPUTING",
    "supermarket": "SUPERMARKET",
    "babyproducts": "BABY_PRODUCTS",
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
    try:
        object_id = ObjectId(product_id)
    except bson.errors.InvalidId:
        return None, None

    for collection_name in database.list_collection_names():
        collection = database[collection_name]
        product = collection.find_one({"_id": object_id})  # Ensure ObjectId is used
        if product:
            return product, collection
    return None, None


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
            "link": product_link,
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
    if not link.startswith("http://") and not link.startswith("https://"):
        print(f"Invalid URL: {link}")
        return None

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
        images = soup.select("div.details img")
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
@login_required
def home():
    if request.method == "GET":
        search = request.args.get("searchProduct")
        if search:
            # Save search history
            email = session.get("email")
            users_collection.update_one(
                {"email": email},
                {"$push": {"search_history": {"search_term": search, "timestamp": datetime.datetime.now()}}}
            )

            print(search)
            search_results = search_products(search)
            return render_template("search_results.html", products=search_results, search_term=search)
        else:
            pass
    return render_template("home.html", email=session.get("name"))


@app.route("/<category>", methods=["GET", "POST"])
def show_category(category):
    if category not in valid_collections:
        return redirect(url_for("home")), 404

    collection_name = valid_collections[category]
    jumia_instance = get_products(database_jumia, category)
    products = jumia_instance
    return render_template("category.html", category=category.replace("-", " ").title(),
                           products=products, email=session.get("name"))


@app.route("/product/<product_id>", methods=["GET", "POST"])
@login_required
def product_page(product_id):
    if not product_id:
        return "Product ID is missing", 400

    try:
        product, collection = get_product_by_id(database_jumia, product_id) or get_product_by_id(database_kil, product_id)
    except bson.errors.InvalidId:
        return "Invalid product ID format", 400

    if not product:
        return "Product not found", 404

    detailed_product = scrape_product_details(product['product_link'])
    if not detailed_product:
        # Delete the product from the database
        result = collection.delete_one({"_id": ObjectId(product_id)})
        flash("Could not retrieve product details. The product has been removed.", "danger")
        return redirect(url_for("home"))

    related_products = get_related_products(product.get("category", ""))

    if request.method == "POST":
        if 'find_cheapest' in request.form:
            product_name = request.form.get("name")
            compare = Compare(product_name)
            compare.compare(product_name)

            def extract_price(price_str):
                """Helper function to convert price strings to float."""
                if isinstance(price_str, str):
                    return float(price_str.replace('KSh', '').replace(',', '').strip())
                elif isinstance(price_str, float):
                    return price_str
                else:
                    raise ValueError(f"Unexpected price format: {price_str}")

            cheapest = None
            jumia = None
            kilimal = None

            try:
                if cheapest_in_jumia:
                    product1 = cheapest_in_jumia[0]
                    jumia = scrape_product_details(product1["link"])
            except Exception as e:
                flash(f"Error retrieving product from Jumia: {str(e)}", "danger")

            try:
                if cheapest_in_kilimal:
                    product2 = cheapest_in_kilimal[0]
                    kilimal = product2
            except Exception as e:
                flash(f"Error retrieving product from Kilimall: {str(e)}", "danger")

            if jumia and kilimal:
                jumia_price = extract_price(jumia["price"])
                kilimal_price = extract_price(kilimal["price"])
                cheapest = jumia if jumia_price <= kilimal_price else kilimal
            elif jumia:
                cheapest = jumia
            elif kilimal:
                cheapest = kilimal

            if not cheapest:
                flash("No products found in Jumia or Kilimall", "warning")

            return render_template(
                "compare.html",
                product1=jumia,
                product2=kilimal,
                cheapest_product=cheapest
            )
        else:
            # Handle add to cart or view product form submission here
            pass

    return render_template("product_page.html", product=detailed_product,
                           related_products=related_products, email=session.get("name"))

@app.route("/login", methods=["GET", "POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        checkmail = users_collection.find_one({"email": email})
        if checkmail:
            try:
                if pbkdf2_sha256.verify(password, checkmail["password"]):  # Correct password verification
                    session["email"] = email
                    session["name"] = checkmail["name"]
                    return redirect(url_for("home"))
                else:
                    flash("Invalid email or password")
                    return render_template("login.html", email=email)
            except ValueError:
                flash("Invalid email or password")
                return render_template("login.html", email=email)
        else:
            flash("Invalid email or password")
            return render_template("login.html", email=email)

    return render_template("login.html", email=email)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        if password != confirmpassword:
            flash("Passwords do not match")
            return redirect(url_for("register"), code=302)
        else:
            userdata = {"name": name, "email": email, "password": pbkdf2_sha256.hash(password)}
            users_collection.insert_one(userdata)
            session["email"] = email
            session["name"] = name
            flash("Registered Successfully", "success")

            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    email = session.get("email")
    user = users_collection.find_one({"email": email})

    if request.method == "POST":
        # Update profile details
        name = request.form.get("name")
        if name:
            users_collection.update_one({"email": email}, {"$set": {"name": name}})
            session["name"] = name
            flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)


@app.route("/search_history")
@login_required
def search_history():
    email = session.get("email")
    user = users_collection.find_one({"email": email})
    search_history = user.get("search_history", [])
    return render_template("search_history.html", search_history=search_history)


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    email = session.get("email")
    user = users_collection.find_one({"email": email})

    if request.method == "POST":
        # Update preferences
        preference = request.form.get("preference")
        users_collection.update_one({"email": email}, {"$set": {"preferences": preference}})
        flash("Preferences updated successfully.", "success")
        return redirect(url_for("preferences"))

    # Generate preferences from search history
    search_history = user.get("search_history", [])
    search_count = {}
    for entry in search_history:
        search_term = entry.get("search_term")
        if search_term:
            search_count[search_term] = search_count.get(search_term, 0) + 1

    # Add frequently searched products to preferences
    sorted_searches = sorted(search_count.items(), key=lambda x: x[1], reverse=True)
    top_preferences = [search for search, count in sorted_searches if count > 1]

    # Save top preferences
    users_collection.update_one({"email": email}, {"$set": {"preferences": top_preferences}})

    preferences = user.get("preferences", [])
    return render_template("preferences.html", preferences=preferences)


@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)


if __name__ == "__main__":
    app.run(debug=True)
