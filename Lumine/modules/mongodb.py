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
        post_dict = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No", "Guild_Status": "No", "Vault": "No"}
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

"""
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
    collection.update_one({"_id": sender_id}, {"$set": {"Guild": bio[1], "Guild_Status": "Creator", "Vault": "100"}})
    message.reply_text("Created a new guild!")
"""    
      
#/points
def pointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    #post_dict = {"_id": sender_id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No", "Guild_Status": "No"}
    results = collection.find_one({"_id": sender_id})
    result = str(results["Points"])
    message.reply_text(result)


#/setpoints
@gods_plus
def setpointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        point1 = list_of_words[1]
        points1 = int(point1)
        collection.update_one({"_id": user_id}, {"$inc": {"Points": points1}})
        message.reply_text("successfully updated the points")
        
    if len(list_of_words) == 3:
        id_tag = list_of_words[1]
        point2 = list_of_words[2]
        points2 = int(point2)
        collection.update_one({"_id": id_tag}, {"$inc": {"Points": points2}})
        message.reply_text("successfully updated the points")
        
    elif len(list_of_words) == 2:
        point3 = list_of_words[1]
        points3 = int(point3)
        collection.update_one({"_id": sender_id}, {"$inc": {"Points": points3}})
        message.reply_text("successfully updated the points")
            

#/deposit <amount>
def depositx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    points = int(list_of_words[1])
    
    if len(list_of_words) == 2:
        results1 = collection.find_one({"_id": sender_id})
        result1 = int(results["Points"])
        result2 = str(results["Guild"])
        
        if result2 == "No":
            message.reply_text("Brooooooooooo,\nJoin a guild first to have a vault")
        else :
            if points < result1:
                collection.update_many({"Guild": result2}, {"$inc": {"Vault": points}})
                message.reply_text("Deposited points!")
            else:
                message.reply_text("you dont have enough points to deposit")
    else:
        message.reply_text("Provide me something to deposit")


#/leaderboard
def leaderboardx(update: Update, context: CallbackContext):
    leaderboardr = collection.find({}).sort({Points:-1}).limit(10)
    leaderboardrs = str(leaderboardr)
    message.reply_text(leaderboardrs)

"""
mydoc = mycol.find().sort("name")
aggregate([
{$group:{_id:"$Appname", softcount:{$max:"$softcount"}}},
{$project:{_id:0, "Appname":"$_id", softcount:1}},
{$sort:{softcount:-1}},
{$limit: 5}
])        
"""
#CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", createguildx, run_async=True)
POINTS_HANDLER = DisableAbleCommandHandler("point", pointsx, run_async=True)
SETPOINTS_HANDLER = DisableAbleCommandHandler("setpoints", setpointsx, run_async=True)
DEPOSIT_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)
LEADERBOARDX_HANDLER = DisableAbleCommandHandler("leaderboard", leaderboardx, run_async=True)

#dispatcher.add_handler(CREATEGUILD_HANDLER)
dispatcher.add_handler(POINTS_HANDLER)
dispatcher.add_handler(SETPOINTS_HANDLER)
dispatcher.add_handler(DEPOSIT_HANDLER)
dispatcher.add_handler(LEADERBOARDX_HANDLER)
