from datetime import datetime
from Lumine import dispatcher, DEV_USERS, OWNER_ID
from Lumine.modules.mongodb import collection
import time
from telegram.ext.dispatcher import run_async
from pymongo import MongoClient
from telegram import InlineKeyboardButton, ParseMode, InlineKeyboardMarkup, Update, MessageEntity
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, run_async
from Lumine.modules.helper_funcs.chat_status import sudo_plus, gods_plus
from Lumine.modules.helper_funcs.extraction import extract_user

TESTX_IMG = "https://te.legra.ph/file/dc9325a322b1c8981eaf7.jpg"


#/create <guild name>
@gods_plus
def createguildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
    first_name = update.effective_user.first_name
    mention = f'<a href="tg://user?id={sender_id}">{first_name}</a>'
    bio = text.split(
        None, 1
    )
    guild_name = bio[1]
    guild_request = f"""
<b>#GUILD_REQUEST :
USER : [{first_name}](tg://openmessage?user_id={sender_id})
USER ID : {sender_id}
GUILD NAME : {guild_name}</b>
"""
    bio = text.split(
        None, 1
    )
    #collection.update_one({"_id": sender_id}, {"$set": {"Guild": bio[1], "Guild_Status": "Creator"}})
    message.reply_text("YOUR Request has been sent")
    dispatcher.bot.send_photo(f"@suppportXd", photo=REQUEST_IMG, caption=f"{guild_request}", parse_mode=ParseMode.HTML)


    
    


CREATE_HANDLER = CommandHandler("createguild", createguildx)

dispatcher.add_handler(CREATE_HANDLER)
