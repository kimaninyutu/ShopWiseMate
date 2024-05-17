from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
uri = ("mongodb+srv://kimanihezekiah:Kimani_4802@cluster0.w7vjsqj.mongodb.net/?retryWrites=true&w=majority&appName"
       "=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Jumia"]


phoneTablets = database["phoneTablets"]
for x in phoneTablets.find({"name": {"$regex":'^Smart Watch'}}):
    print(x)







