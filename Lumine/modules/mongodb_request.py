import json
import html
from datetime import datetime
from Lumine import dispatcher, DEV_USERS, OWNER_ID, EVENT_LOGS
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

GUILD_IMG = "https://te.legra.ph/file/dc9325a322b1c8981eaf7.jpg"
JOB_IMG = "https://te.legra.ph/file/dc9325a322b1c8981eaf7.jpg"


#/create <guild name>
@typing_action
def createguildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    list_of_words = message.text.split(" ")
    bot = context.bot
    log_message = ""
    first_name = update.effective_user.first_name
    guild_name = list_of_words[1]

    log_message = (
        f"#<b>GUILD_REQUEST</b>\n"
        f"User: {mention_html(sender_id, html.escape(first_name))}\n"
        f"User ID: {sender_id}\n"
        f"Guild Name: {guild_name}"
    )
        
    if EVENT_LOGS:
        try:
            log = bot.send_photo(
                EVENT_LOGS, GUILD_IMG,caption=log_message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Request",
                                url=f"t.me/friendsdomain/{message.message_id}"
                            )
                        ]
                    ]
                )
            )

        except BadRequest as excp:
            log = bot.send_message(
                EVENT_LOGS,log_message +
                "\n\nFormatting has been disabled due to an unexpected error.")
            
    message.reply_text(
        "Your <b>Guild</b> Request has been sent to the ministry",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Your Request",
                        url=f"t.me/eventlogsforeri/{log.message_id}"
                    )
                ]
            ]
        ),
    )
    
#/takejob
@typing_action
def takejobx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    list_of_words = message.text.split(" ")
    bot = context.bot
    log_message = ""
    first_name = update.effective_user.first_name
    postx_name = list_of_words[1]

    log_message = (
        f"#<b>JOB_REQUEST</b>\n"
        f"User: {mention_html(sender_id, html.escape(first_name))}\n"
        f"User ID: {sender_id}\n"
        f"Post: {postx_name}"
    )
        
    if EVENT_LOGS:
        try:
            log = bot.send_photo(
                EVENT_LOGS, JOB_IMG,caption=log_message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Request",
                                url=f"t.me/friendsdomain/{message.message_id}"
                            )
                        ]
                    ]
                )
            )

        except BadRequest as excp:
            log = bot.send_message(
                EVENT_LOGS,log_message +
                "\n\nFormatting has been disabled due to an unexpected error.")
            
    message.reply_text(
        "Your <b>JOB</b> Request has been sent to the ministry",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Your Request",
                        url=f"t.me/eventlogsforeri/{log.message_id}"
                    )
                ]
            ]
        ),
    )
    



CREATEX_HANDLER = CommandHandler("createguild", createguildx, run_async=True)
TAKEJOB_HANDLER = CommandHandler("takejob", takejobx, run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)
#_HANDLER = CommandHandler("", , run_async=True)


dispatcher.add_handler(CREATEX_HANDLER)
dispatcher.add_handler(TAKEJOB_HANDLER)
dispatcher.add_handler(TAKEJOB_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
