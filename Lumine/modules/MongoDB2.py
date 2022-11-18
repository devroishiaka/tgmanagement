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



def datatype(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    typeaa = type(user_id)
    typecc = type(chat_id)
    typeuu = type(user_name)
    splitters = message.text.split(" ")
    if len(splitters) > 1:
        words = splitters[1]
        wrodsss = message.text.split(None, 1)[1]
        typess = type(words)
        typessss = type(wrodsss)
        message.reply_text(f"User ID = {user_id}\nTYPE = {typeaa}\n\nChat ID = {chat_id}\nTYPE = {typecc}\n\nUser Name = {user_name}\nTYPE = {typeuu}\n\nSENT MESSAGE(space) = {words}\nTYPE = {typess}\n\nSENT MESSAGE(None) = {wrodsss}\nTYPE = {typessss}")
    else:
        message.reply_text(f"User ID = {user_id}\nTYPE = {typeaa}\n\nChat ID = {chat_id}\nTYPE = {typecc}\n\nUser Name = {user_name}\nTYPE = {typeuu}")

def testdevs1(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    collection1.insert_one({"_id": user_id, "weapons": ["katana", "shurikin", "berakhuda sword"]})
    message.reply_text("Done")

def testdevs2(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    result = collection1.find_one({"_id": user_id})
    weapons = result["weapons"]
    weapons1 = weapons[0]
    weapons2 = weapons[1]
    weapons3 = weapons[2]
    message.reply_text(f"Done\n{weapons1}\n{weapons2}\n{weapons3}")

DATATYPE_HANDLER = DisableAbleCommandHandler("datatype", datatype, run_async=True)
testdevs1_HANDLER = DisableAbleCommandHandler("testdevs1", testdevs1, run_async=True)
testdevs2_HANDLER = DisableAbleCommandHandler("testdevs2", testdevs2, run_async=True)

dispatcher.add_handler(DATATYPE_HANDLER)
dispatcher.add_handler(testdevs1_HANDLER)
dispatcher.add_handler(testdevs2_HANDLER)
