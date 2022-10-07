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
"""
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
"""

from Lumine.mongoinit import DataBase

database = DataBase(
    connection_string = f'mongodb+srv://ishikki:ishikki143@cluster0.gafny.mongodb.net/Cluster0?retryWrites=true&w=majority',
    db_name = cluster0,
)


def send_start_message(message):
    database.register_user(message)
    bot.send_message(message.chat.id, 'Какое-то стартовое сообщение')

def send_sub(message):
    database.subscribe_user(message)
    bot.send_message(message.chat.id, 'Ты подписан')

    """
def send_unsub(message):
    database.unsubscribe_user(message)
    bot.send_message(message.chat.id, 'Ты отписан, лох')

@bot.message_handler(commands=['get_all_users_identificators'])
def test1(message):
    msg = ' '.join(map(str, database.get_all_users_identificators()))
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(commands=['get_all_users'])
def test2(message):
    msg = ' '.join(map(str, database.get_all_users_data()))
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(commands=['get_subscribed_users_data'])
def test10(message):
    msg = ' '.join(map(str, database.get_subscribed_users_data()))
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(commands=['get_subscribed_users_identificators'])
def test15(message):
    msg = ' '.join(map(str, database.get_subscribed_users_identificators()))
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(commands=['check_my_status'])
def test3(message):
    bot.send_message(message.from_user.id, database.check_subscription_status_for_user(message.chat.id))

@bot.message_handler(commands=['stats'])
def test4(message):
    bot.send_message(message.from_user.id, str(database.get_subscription_stats()))

bot.polling(none_stop=True)"""
    
REGI_HANDLER = CommandHandler(("regi"), send_start_message)
dispatcher.add_handler(REGI_HANDLER)
