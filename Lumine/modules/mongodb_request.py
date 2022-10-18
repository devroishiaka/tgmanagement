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
#GUILD_REQUEST :
USER : {mention}
USER ID : {sender_id}
GUILD NAME : {guild_name}
"""

    #collection.update_one({"_id": sender_id}, {"$set": {"Guild": bio[1], "Guild_Status": "Creator"}})
    message.reply_text("YOUR Request has been sent")
    dispatcher.bot.send_photo(f"@suppportXd", photo=REQUEST_IMG, caption=guild_request, parse_mode=ParseMode.HTML)
"""
def createguildxx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    guild_request = f
#GUILD_REQUEST :
USER : 
USER ID : 
GUILD NAME : 

    message.reply_text("YOUR Request has been sent")
    dispatcher.bot.send_photo(f"@logsforfriendsdomain", photo=TESTX_IMG, caption=guild_request, parse_mode=ParseMode.HTML)
"""
    
#/takejob
def takejobx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
    first_name = update.effective_user.first_name
    bio = text.split(
        None, 1
    )
    jon_name = bio[1]
    job_request = f"""
#JOB_REQUEST :
USER : {first_name}
USER ID : {sender_id}
REQUESTED JOB :
{jon_name}
"""
    message.reply_text("Your JOB Request has been sent")
    dispatcher.bot.send_photo(f"@logsforfriendsdomain", photo=TESTX_IMG, caption=job_request, parse_mode=ParseMode.HTML)


def testingx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
 
    mesid2 = message.message.id
    first_name = update.effective_user.first_name
    user_namm = update.effective_user.user_name
    job_request = "HELLO,\nJust testing"
    dispatcher.bot.send_photo(f"@logsforfriendsdomain", photo=TESTX_IMG, caption=job_request, parse_mode=ParseMode.HTML, reply_markup = InlineKeyboardMarkup([InlineKeyboardButton("Your request", url = f"https://t.me/friendsdomain/{mesid2}")]))
    message.reply_text(f"Done {first_name}\n yo @{user_namm}", reply_markup = InlineKeyboardMarkup([InlineKeyboardButton("Your request", url = f"https://t.me/friendsdomain/{mesid2}")]))
    
    #https://t.me/Friendsdomain/15588

CREATE_HANDLER = CommandHandler("createguild", testingx)
#CREATEX_HANDLER = CommandHandler("createguildx", createguildxx)
TAKEJOB_HANDLER = CommandHandler("takejob", takejobx)

dispatcher.add_handler(CREATE_HANDLER)
#dispatcher.add_handler(CREATEX_HANDLER)
dispatcher.add_handler(TAKEJOB_HANDLER)
