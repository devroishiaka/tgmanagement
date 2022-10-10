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
async def get_points(sender_id: int):
    user = collection.find_one({"_id": sender_id})
    if user:
        user = user["Points"]
    else:
        user = {}
    return user
"""
#----------------------------------#######################
#/register [name]
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/register"))
async def register(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    if len(list_of_words) == 1:
        return await event.respond(
            "Give me a name in the format /register <Your Name>"
        )
    
    results = collection.find({"_id": sender.id})
    if results:
        return await event.respond(
            "You already registered in My Database"
        )
    else :
        name = list_of_words[1]
        post_dict = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No"}
        collection.insert_one(post_dict)
        
        await event.reply("Successfully Registered!!!")

#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def join(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    guild = list_of_words[1]

    collection.update_one({"_id": sender.id}, {"$set":{"Guild": guild}})

    textx = "Successfully joined the guild {} !!!"
    await event.reply(textx.format(guild), parse_mode=ParseMode.MARKDOWN)


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
    message.reply_text("Created a new guild!")
    
CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", createguild, run_async=True)
dispatcher.add_handler(CREATEGUILD_HANDLER)
      

#/points
def points(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    #post_dict = {"_id": sender_id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No"}
    results = collection.find_one({"_id": sender_id})
    result = str(results["Points"])
    message.reply_text(result)

POINTS_HANDLER = DisableAbleCommandHandler("point", points, run_async=True)
dispatcher.add_handler(POINTS_HANDLER)
