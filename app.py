from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# MongoDB connection
uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Jumia"]

# Define valid collections
valid_collections = {
    "phones-tablets": "PHONE_TABLETS",
    "electronics": "ELECTRONICS",
    "home-office-appliances": "APPLIANCES",
    "health-beauty": "HEALTH_BEAUTY",
    "home-office": "HOME_OFFICE",
    "fashion": "FASHION",
    "computing": "COMPUTING",
    "supermarket": "SUPERMARKET",
    "baby-products": "BABY_PRODUCTS",
    "sporting-goods": "sporting-goods",
    "automobile": "AUTOMOBILE",
    "video-games": "GAMING",
    "patio-lawn-garden": "GARDEN_OUTDOOR",
    "books-movies-music": "BOOKS_MOVIE_MUSIC",
    "livestock": "LIVESTOCK",
    "industrial-scientific": "INDUSTRIAL_SCIENTIFIC",
    "miscellaneous": "MISCELLANEOUS",
    "musical-instruments": "MUSICAL_INSTRUMENTS",
    "pet-supplies": "PET_SUPPLIES",
    "services": "SERVICES",
    "toys-games": "TOYS_GAMES",
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

    products = db[valid_collections[category]].find()
    return render_template("category.html", category=category.replace("-", " ").title(), products=products)


@app.route("/jumia")
def show_jumia():
    return render_template("home.html")

@app.route("/kilimall")
def show_kilimall():
    return render_template("home.html")


@app.route("/sporting-goods")
def show_sportinggoods():
    return render_template("base2.html")


if __name__ == "__main__":
    app.run(debug=True)
