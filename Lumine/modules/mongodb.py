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

#----------------------------------#######################----------------------------------

#----------------------------------#######################----------------------------------
#/register [name]
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/register"))
async def registerx(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    if len(list_of_words) == 1:
        return await event.respond(
            "Give me a name in the format /register <Your Name>"
        )
    
    results = collection.find_one({"_id": sender.id})
    if results :
        return await event.respond(
            "You already registered in My Database"
        )
    else :
        name = list_of_words[1]
        post_dict = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No", "Guild_Status": "No"}
        collection.insert_one(post_dict)
        
        await event.reply("Successfully Registered!!!")

#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def joinx(event):
    sender = await event.get_sender()
    SENDER = sender.id
    
    list_of_words = event.message.text.split(" ")
    guild = list_of_words[1]

    collection.update_one({"_id": sender.id}, {"$set":{"Guild": guild}})

    textx = "Successfully joined the guild {} !!!"
    await event.reply(textx.format(guild), parse_mode=ParseMode.MARKDOWN)


#/create <guild name>
@gods_plus
def createguildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
    bio = text.split(
        None, 1
    )
    collection.update_one({"_id": sender_id}, {"$set": {"Guild": bio[1], "Guild_Status": "Creator"}})
    message.reply_text("Created a new guild!")
    
      

#/points
def pointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    #post_dict = {"_id": sender_id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No", "Guild_Status": "No"}
    results = collection.find_one({"_id": sender_id})
    result = str(results["Points"])
    message.reply_text(result)




@gods_plus
def setpointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    point3 = list_of_words[1]
    points = int(point3)

    collection.update_one({"_id": sender_id}, {"$inc": {"Points": points}})
    message.reply_text("successfully updated the points")
            
            
"""            
    if len(list_of_words) == 1:
        message.reply_text("atleast provide me some points to update")
    
    results = collection.find({"_id": sender_id})
    if results:
        #collection.update_one({"_id": sender_id}, {"$set": {"Guild": bio[1], "Guild_Status": "Creator"}})
        collection.update_one({"_id": sender_id}, {"$inc": {"Points": 
        message.reply_text("Successfully updated points")
    else :
        message.reply_text("No such user registerd in my database!")
"""
                                               


CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", createguildx, run_async=True)
POINTS_HANDLER = DisableAbleCommandHandler("point", pointsx, run_async=True)
SETPOINTS_HANDLER = DisableAbleCommandHandler("setpoints", setpointsx, run_async=True)

dispatcher.add_handler(CREATEGUILD_HANDLER)
dispatcher.add_handler(POINTS_HANDLER)
dispatcher.add_handler(SETPOINTS_HANDLER)


