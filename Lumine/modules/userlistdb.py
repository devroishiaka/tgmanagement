import html
import os
from typing import Optional
import pymongo
from pymongo import MongoClient
from Lumine.mongodb import collection
from Lumine import (
    dispatcher,
)
from Lumine.userlist import (
    GODS,
    SCLASS,
    ACLASS,
    BCLASS,
    CCLASS,
    DCLASS,
)
from Lumine.modules.helper_funcs.extraction import extract_user
from telegram import Update, ParseMode, MessageEntity, MAX_MESSAGE_LENGTH
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.utils.helpers import mention_html, escape_markdown
from telegram.ext.dispatcher import run_async

#--------------------------------------------------------------#
#post1 = {"_id": 1, "name": "shikumi", "score": 200}

#collection.insert_one(post1)  #single
#--------------------------------------------------------------#

def registerx(update: Update, context: CallbackContext):
    args = context.args
    user_id = extract_user(update.effective_message, args)
    first_name = update.effective_user.first_name
    post = {"_id": {user.id}, "Name": "{html.escape(user.first_name)}", "Points": 100, "Guild": "null"}
    return collection.insert_one(post)

REGISTERX_HANDLER = CommandHandler(("register"), registerx)
dispatcher.add_handler(REGISTERX_HANDLER)
