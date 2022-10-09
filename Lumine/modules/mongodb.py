import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from pymongo import MongoClient
from Lumine import dispatcher
from Lumine import telethn as LumineTelethonClient
from Lumine.modules.helper_funcs.misc import delete

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown, mention_html
from Lumine import (
    DEV_USERS,
    OWNER_ID,
    SUDO_USERS,
    SUPPORT_USERS,
    WHITELIST_USERS,
    INFOPIC,
    dispatcher,
    sw,
)
from Lumine.modules.helper_funcs.chat_status import sudo_plus, gods_plus
from Lumine.modules.helper_funcs.extraction import extract_user
from Lumine.modules.disable import DisableAbleCommandHandler

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

    await event.reply("Successfully Registered!!!")

#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    guild = list_of_words[1]

    collection.update_one({"_id": sender.id}, {"$set":{"Guild": guild}})

    await event.reply("Successfully joined the guild {guild}!!!")


#/create <guild name>

@gods_plus
def createguild(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
    bio = text.split(
        None, 1
    )
    collection.update_one({"_id": sender_id}, {"$set":{"Guild": bio[1]}})
    message.reply_text("Updated points!")
    
CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", createguild, run_async=True)
dispatcher.add_handler(CREATEGUILD_HANDLER)
"""
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
"""
