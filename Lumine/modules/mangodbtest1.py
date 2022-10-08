from datetime import datetime
from asyncio import sleep
from telethon import events
from pymongo import MongoClient
from bson.objectid import objectid  #bson
from Lumine import dispatcher
from Lumine import telethn as LumineTelethonClient
from Lumine.modules.helper_funcs.misc import delete


url = "mongodb+srv://ishikki:ishikki143@cluster0.azewvhf.mongodb.net/?retryWrites=true&w=majority"
cluster = MangoClient(url) 

db = cluster["Cluster0"]
collection = db["userlistx"]

#----------------------------------#######################

#/register [name]
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/registerxy"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split("")
    name = list_of_words[1]
    dt_string = datetime.now()strftime("%d-%m_%y")
    post_dict = {"Name": name, "points": 100, "Guild": "Null" "date": dt_string}

    collection.insert_one(post_dict)

    text = "Successfully Registered!!!"
    await client.send_message(SENDER, text, parse_mode='html')
