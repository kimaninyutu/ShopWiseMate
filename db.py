import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Jumia"]

# Get the list of collection names
collection_names = database.list_collection_names()


def kim():
    for collection_name in collection_names:
        collection = database[collection_name]
        print(f"Retrieving documents from collection: {collection_name}")

        # Retrieve specific fields from each document in the collection
        documents = collection.find({},
                                    {"name": 1,
                                     "product_link": 1,
                                     "price": 1,
                                     "rating": 1,
                                     "image": 1,
                                     "other_images": 1,
                                     "product_descriptions": 1})

        # Print each document
        for document in documents:
            print(document)


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
    for document in documents:
        print(document)


get_products("appliances")
