from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection
uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Jumia"]

# Get the list of collection names
collection_names = database.list_collection_names()


def get_products(collection_name):
    products = []
    collection = database[collection_name]
    print(f"Retrieving documents from collection: {collection_name}")

    # Retrieve specific fields from each document in the collection
    documents = collection.find({}, {
        "name": 1,
        "product_link": 1,
        "price": 1,
        "rating": 1,
        "image": 1,
        "other_images": 1,
        "product_descriptions": 1
    })

    # Append each document (product) to the products list
    count = 0
    for document in documents:
        count += 1
        if count >= 500:
            break
        else:

            products.append(document)

    return products


# Define valid collections
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


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/<category>")
def show_category(category):
    if category not in valid_collections:
        return "Category not found", 404

    # Get the name of the collection corresponding to the category
    collection_name = valid_collections[category]

    # Use the Jumia class to fetch products from the specified collection
    jumia_instance = get_products(category)

    products = jumia_instance
    print(products)

    # Render the category.html template with the fetched products
    return render_template("category.html", category=category.replace("-", " ").title(), products=products)


@app.route("/jumia")
def show_jumia():
    return render_template("home.html")


@app.route("/kilimall")
def show_kilimall():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
    app.run(development=True)
