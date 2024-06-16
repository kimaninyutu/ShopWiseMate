from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection for Jumia
uri_jumia = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
             "=Cluster0")
client_jumia = MongoClient(uri_jumia, server_api=ServerApi('1'))
database_jumia = client_jumia["Jumia"]
collection_names_jumia = database_jumia.list_collection_names()

# MongoDB connection for Kil
uri_kil = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
           "=Cluster0")
client_kil = MongoClient(uri_kil, server_api=ServerApi('1'))
database_kil = client_kil["Kil"]
collection_names_kil = database_kil.list_collection_names()

def get_products(database, collection_name):
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
    })

    count = 0
    for document in documents:
        count += 1
        if count >= 500:
            break
        else:
            products.append(document)

    return products

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

@app.route("/<category>")
def show_category(category):
    if category not in valid_collections:
        return "Category not found", 404

    collection_name = valid_collections[category]

    jumia_instance = get_products(database_jumia, category)
    products = jumia_instance
    print(products)

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
