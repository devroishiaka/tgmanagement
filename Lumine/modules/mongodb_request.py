import json
import html
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
from telegram.utils.helpers import mention_html
from Lumine.modules.helper_funcs.alternate import typing_action
from Lumine.modules.log_channel import gloggable

TESTX_IMG = "https://te.legra.ph/file/dc9325a322b1c8981eaf7.jpg"


#/create <guild name>
@typing_action
@gods_plus
@gloggable
def createguildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    list_of_words = message.text.split(" ")
    bot = context.bot
    log_message = ""
    first_name = update.effective_user.first_name
    #mention = f'<a href="tg://user?id={sender_id}">{first_name}</a>'
    guild_name = list_of_words[1]

    message.reply_text(
        "YOUR Request has been sent [hmm](t.me/ishikki_akabane)",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Request",
                        url=f"t.me/logsforfriendsdomain/"
                    )
                ]
            ]
        ),
    )
    log_message = (
        f"#GUILD_REQUEST"
        f"<b>USER:</b> {mention_html(sender_id, html.escape(first_name))}\n"
        f"<b>USER ID:</b> {sender_id}\n"
        f"<b>GUILD NAME:</b> {guild_name}"
    )
        
    if EVENT_LOGS:
        try:
            log = bot.send_photo(
                EVENT_LOGS, TESTX_IMG,caption=log_message, parse_mode=ParseMode.HTML)
        except BadRequest as excp:
            log = bot.send_message(
                EVENT_LOGS,log_message +
                "\n\nFormatting has been disabled due to an unexpected error.")

    
    
#/takejob
def takejobx(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(
        "Your JOB Request has been sent",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Request",
                        url=f"t.me/friendsdomain"
                    )
                ]
            ]
        ),
    )
    


def testingx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    text = message.text
    first_name = update.effective_user.first_name
    user_namm = update.effective_user.user_name
    job_request = "HELLO, Just testing"
    dispatcher.bot.send_photo(f"@logsforfriendsdomain", photo=TESTX_IMG, caption=job_request, parse_mode=ParseMode.HTML)
    message.reply_text(f"Done {first_name}\n yo @{user_namm}", reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Your request", url = f"https://t.me/friendsdomain/{message.message_id}")]]))
    
    #https://t.me/Friendsdomain/15588

#CREATE_HANDLER = CommandHandler("createguild", testingx)
CREATEX_HANDLER = CommandHandler("createguild", createguildx, run_async=True)
TAKEJOB_HANDLER = CommandHandler("takejob", takejobx, run_async=True)

#dispatcher.add_handler(CREATE_HANDLER)
dispatcher.add_handler(CREATEX_HANDLER)
dispatcher.add_handler(TAKEJOB_HANDLER)
