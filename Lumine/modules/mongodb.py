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
"""
def create_message_select_query(ans):
    text = ""
    for res in ans:
        if res in ans:
            if(res !=[]):
                id = res["_id"]
                name = res["Name"]
                level = res["Level"]
                rank = res["Rank"]
                points = res["Points"]
                guild = res["Guild"]
                text+= "<b>"+ str(id) + "</b>"+ str(name) + "</b>"+ str(level) + "</b>"+ str(rank) + "</b>"+ str(points) + "</b>"+ str(guild) + "</b>"
    message = "info\n"+text
    return message
"""

#----------------------------------#######################
#/register [name]
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/register"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    name = list_of_words[1]
    post_dict = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No"}

    collection.insert_one(post_dict)

    text = "Successfully Registered!!!"
    await event.reply("Successfully Registered!!!")

#/points
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/points"))
async def points(event):
    sender = await event.get_sender()
    SENDER = sender.id
    #post_dict = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class" "Points": 100, "Guild": "No"}
    results = collection.find_one({"_id": sender.id})
    #pointx = results["Points"]
    #text1 = create_message_select_query(results)
    await event.reply(results)
