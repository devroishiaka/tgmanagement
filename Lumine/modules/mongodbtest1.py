import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from pymongo import MongoClient
from Lumine import dispatcher
from Lumine import telethn as LumineTelethonClient
from Lumine.modules.helper_funcs.misc import delete


url = "mongodb+srv://ishikki:ishikki143@cluster0.azewvhf.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(url) 

db = cluster['userlistxy']
collection = db['userdataxy']

#----------------------------------#######################

#/register [name]

@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/registerxy"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    name = list_of_words[1]
    post_dict = {"Name": name, "points": 100, "Guild": "No"}

    collection.insert_one(post_dict)

    text = "Successfully Registered!!!"
    await LumineTelethonclient.send_message(SENDER, text, parse_mode='html')

