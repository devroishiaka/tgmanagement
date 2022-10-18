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

def partnerx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    sender_name = update.effective_user.first_name

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        user_name = repl_message.from_user.first_name
        message.reply_text(f"OK\n{user_name} is now your partner\nHappy married life {sender_name} and {user_name}")
    else:
        message.reply_text("reply to someone")

#CREATEGUILD_HANDLER = DisableAbleCommandHandler("createguild", partnerx, run_async=True)
POINTS_HANDLER = DisableAbleCommandHandler("partner", partnerx, run_async=True)

dispatcher.add_handler(POINTS_HANDLER)
