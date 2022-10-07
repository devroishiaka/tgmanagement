import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://ishikki:ishikki143@cluster0.azewvhf.mongodb.net/?retryWrites=true&w=majority")

db = cluster["cluster0"]
collection = db["userlistx"]
