import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from pymongo import MongoClient
from Lumine import dispatcher
from Lumine import telethn as LumineTelethonClient
from Lumine.modules.helper_funcs.misc import delete

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters, CallbackQueryHandler, run_async
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
#collection1 = --- User Data   ---------post1
#collection2 = --- Guild Data  ---------post2

#post1 =                   #Post2 =
"""
_id =                      _id = 
Name =                     Guild_Name = 
level =                    Guild_Level =
Rank =                     Members =
Points =                   vault =
Gender =                   Guild_Creator =
Partner =                  Crime_Rate =
Friend =                   Guild_Rank = 
Father =                   Guild_Status =
Mother = 
Children = 
Status = (Guild name)
"""
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
        post_dict1 = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Gender": "No", "Partner": "No", "Friend": "No", "Father": "No", "Mother": "No", "Children": "No", "Status": "No", "Bounty": 0}
        collection1.insert_one(post_dict1)
        
        await event.reply("Successfully Registered!!!")


#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def joinx(event):
    sender = await event.get_sender()
    list_of_words = event.message.text.split(" ")
    guild = list_of_words[1]
    registerd = collection1.find_one({"_id": sender.id})
    if registerd:
        guild_exist = collection2.find({"Guild_Name": guild})
        if guild_exist:
            #collection2.update_one({"Guild_Name": guild}, {"$set":{"Guild": guild}})
            collection1.update_one({"_id": sender.id}, {"$set":{"Status": guild}})
            return await event.respond(
            f"🎉 You Successfully joined the {guild} guild!!!"
            )
        else:
            return await event.respond(
            f"{guild} guild dont exist!!"
            )
    else:
        return await event.respond(
        "You not registerd!!\nUse /register to get registerd in this game"
        )


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
    registerd = collection1.find_one({"_id": sender_id})
    if registerd:
        pointreq = int(registerd["Points"])
        if pointreq > 25000:
            collection2.insert_one({"_id": sender_id, "Guild_Name": bio[1], "Guild_Status": "Creator", "Vault": 1000 })
            message.reply_text("Created a new guild!")
        else:
            message.reply_text("You dont have enough points to create the guild")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")

      
#/points
def pointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    #post_dict = {"_id": sender_id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Guild": "No", "Guild_Status": "No"}
    results = collection1.find_one({"_id": sender_id})
    if results:
        result = str(results["Points"])
        message.reply_text(f"Your Total Points are ⊰\n{result}")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")


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
        collection1.update_one({"_id": user_id}, {"$inc": {"Points": points1}})
        message.reply_text("successfully updated the points")
        
    if len(list_of_words) == 3:
        id_tag = list_of_words[1]
        point2 = list_of_words[2]
        points2 = int(point2)
        collection1.update_one({"_id": id_tag}, {"$inc": {"Points": points2}})
        message.reply_text("successfully updated the points")
        
    elif len(list_of_words) == 2:
        point3 = list_of_words[1]
        points3 = int(point3)
        collection1.update_one({"_id": sender_id}, {"$inc": {"Points": points3}})
        message.reply_text("successfully updated the points")
            

#/deposit <amount>
def depositx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    points = int(list_of_words[1])
    registerd = collection1.find_one({"_id": sender_id})
    if registerd:
        if len(list_of_words) == 2:
            results1 = collection1.find_one({"_id": sender_id})
            result1 = int(results["Points"])
            result2 = str(results["Status"])
            if result2 == "No":
                message.reply_text("Brooooooooooo,\nJoin a guild first to have a vault")
            else :
                if points < result1:
                    collection2.update_one({"Guild_Name": result2}, {"$inc": {"Vault": points}})
                    message.reply_text("💸 Successfully Deposited the points!")
                else:
                    message.reply_text("you dont have enough points to deposit")
        else:
            message.reply_text("Provide me something to deposit")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")


#/leaderboard
def leaderboardx(update: Update, context: CallbackContext):
    message = update.effective_message
    #leaderboardr = collection.find({}).sort({Points:-1}).limit(10)
    leaderboardr = collection.find({})
    for result in leaderboardr:
        final = (result["Name"])
        message.reply_text(final)
    #leaderboardrs = str(leaderboardr["Name", "Points"])
    #message.reply_text(result)

#/partner
def partnerx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    sender_name = update.effective_user.first_name
    registerd = collection1.find_one({"_id": sender_id})
    if registerd:
        if message.reply_to_message:
            repl_message = message.reply_to_message
            user_id = repl_message.from_user.id
            user_name = repl_message.from_user.first_name
            rregisterd = collection1.find_one({"_id": user_id})
            if rregisterd:
                collection1.update_one({"_id": sender_id}, {"$set": {"Partner": user_name}})
                collection1.update_one({"_id": user_id}, {"$set": {"Partner": sender_name}})
                message.reply_text(f"🎉Happy Married Life🎉\nCongratulations🎊\n[{sender_name}](tg://openmessage?user_id={sender_id}) ❤ [{user_name}](tg://openmessage?user_id={user_id})")
        

def testt(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(
        "Please choose:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Option a", callback_data=="hmm"),
                    InlineKeyboardButton(text="Option b", callback_data=="hola")
                ]
            ]
        ),
    )
        

def testt_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.effective_message
    msgg = message.edit_text ("hmmm......")
    if query.data == "hmm":
        message.reply_text(f"YOU choose {query.data}")
        msgg.delete()
    if query.data == "hola":
        bot.answer_callback_query(query.id, text="You don't have enough rights to unmute people", show_alert=True)


#CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", createguildx, run_async=True)
POINTS_HANDLER = DisableAbleCommandHandler("point", pointsx, run_async=True)
SETPOINTS_HANDLER = DisableAbleCommandHandler("setpoints", setpointsx, run_async=True)
DEPOSIT_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)
LEADERBOARDX_HANDLER = DisableAbleCommandHandler("leaderboard", leaderboardx, run_async=True)
PARTNER_HANDLER = DisableAbleCommandHandler("partner", partnerx, run_async=True)
TESTT_HANDLER = DisableAbleCommandHandler("testt", testt,run_async=True)
TESTT_BUT_HANDLER = CallbackQueryHandler(testt_callback, pattern=r"hmm",run_async=True)
#_HANDLER = DisableAbleCommandHandler(, , run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)


#dispatcher.add_handler(CREATEGUILD_HANDLER)
dispatcher.add_handler(POINTS_HANDLER)
dispatcher.add_handler(SETPOINTS_HANDLER)
dispatcher.add_handler(DEPOSIT_HANDLER)
dispatcher.add_handler(LEADERBOARDX_HANDLER)
dispatcher.add_handler(PARTNER_HANDLER)
dispatcher.add_handler(TESTT_HANDLER)
dispatcher.add_handler(TESTT_BUT_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
