import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from Lumine import telethn as LumineTelethonClient

from Lumine.modules.MongoDB import collection1, collection2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import (
    dispatcher
)

from Lumine.modules.helper_funcs.chat_status import sudo_plus, gods_plus
from Lumine.modules.helper_funcs.extraction import extract_user
from Lumine.modules.disable import DisableAbleCommandHandler

#----------------------------------#######################----------------------------------
#collection = --- User Data   ---------post1
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
Bounty = 
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
    
    results = collection1.find_one({"_id": sender.id})
    if results :
        return await event.respond(
            "You already registered in My Database"
        )
    else :
        name = list_of_words[1]
        post_dict1 = {"_id": sender.id, "Name": name, "Level": 1, "Rank": "D-Class", "Points": 100, "Gender": "No", "Partner": "No", "Friend": "No", "Father": "No", "Mother": "No", "Children": "No", "Status": "No", "Bounty": 0}
        collection1.insert_one(post_dict1)
        
        await event.reply("Successfully Registered!!!")


      
#/points
def pointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    results = collection1.find_one({"_id": sender_id})
    if results:
        result = str(results["Points"])
        message.reply_text(f"Your Total Points are ⊰\n{result}")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")




#/leaderboard
def leaderboardx(update: Update, context: CallbackContext):
    message = update.effective_message
    leaderboardr = collection.find().sort("Points",-1).limit(10)
    final = "Top Players 🌐\n"
    for result in leaderboardr:
        final += (result["Name"])
        final += " • "
        pointss = str(result["Points"])
        final += (pointss)
        final += "\n"
    message.reply_text(final)
        
    
        

POINTS_HANDLER = DisableAbleCommandHandler("point", pointsx, run_async=True)
DEPOSIT_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)
LEADERBOARDX_HANDLER = DisableAbleCommandHandler("leaderboard", leaderboardx, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)
#_HANDLER = DisableAbleCommandHandler(,run_async=True)



dispatcher.add_handler(POINTS_HANDLER)
dispatcher.add_handler(DEPOSIT_HANDLER)
dispatcher.add_handler(LEADERBOARDX_HANDLER)
#dispatcher.add_handler()
