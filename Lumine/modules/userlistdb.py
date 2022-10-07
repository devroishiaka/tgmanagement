import pymongo
from pymongo import MongoClient
from Lumine.mangodb import collection

#--------------------------------------------------------------#
post1 = {"_id": 1, "name": "shikumi", "score": 200}

collection.insert_one(post1)  #single
