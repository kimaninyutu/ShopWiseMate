from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Jumia"]

for collection in database:
    print(collection)

