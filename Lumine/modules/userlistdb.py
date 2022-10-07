import pymongo
from pymongo import MongoClient

cluster = MangoClient("mongodb+srv://ishikki:ishikki143@cluster0.azewvhf.mongodb.net/?retryWrites=true&w=majority") #mongoURL

db = cluster["cluster0"]  #database name
collection = db["userlistx"]  #collection name

#--------------------------------------------------------------#
post1 = {"_id": 0, "name": "Ishikki", "score": 100}

collection.insert_one(post1)  #single
