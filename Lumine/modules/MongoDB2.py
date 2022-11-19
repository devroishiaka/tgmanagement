import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from Lumine import telethn as LumineTelethonClient

from Lumine.modules.MongoDB import collection1, collection2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler
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
    
def infoxx(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    user_id = int(user_id)
    user_name = update.effective_user.first_name
    registerd = collection1.find_one({"_id": user_id})
    if registerd:
        name = registerd["Name"]
        points = registerd["Points"]
        expp = registerd["EXP"]
        level = registerd["Level"]
        rank = registerd["Rank"]
        guild = registerd["Status"]
        weapons = registerd["Weapons"]
        deposits = registerd["TDeposit"]
        skills = registerd["Skills"]
        bounty = registerd["Bounty"]
        totalduel = registerd["DTotal"]
        achievment = registerd["Achievment"]
        healthno = registerd["Health"]

        healthc = int(healthno) // 10
        health = ""
        for i in range(healthc):
            health += "●"
        for i2 in range(10 - healthc):
            health += "○"
        exppc = int(expp) // 20
        exp = ""
        for i3 in range(exppc):
            exp += "∘"
        for i4 in range(20-exppc):
            exp += "-"
        infofile = ""
        infofile += f"⊱┈「<b> Iɴғᴏ </b>」┈⊰\n"
        infofile += "───────────────────\n"
        infofile += f"EXP: [{exp}]\nLevel ⊸⊱ {level}\n"
        infofile += "───────────────────\n"
        infofile += f"Hᴇᴀʟᴛʜ: [{health}]\n"
        infofile += f"🔹 ID ⊸⊱ {user_id}\n"
        infofile += f"🔹 Nᴀᴍᴇ ⊸⊱ <a href='tg://user?id={user_id}'>{name}</a>\n"
        infofile += f"🔹 Points ⊸⊱ {points}\n"
        infofile += f"🔹 Guild ⊸⊱ {guild}\n\n"
        infofile += f"🔹 Total Deposits ⊸⊱ {deposits}\n"
        infofile += f"🔹 Total Skills ⊸⊱ {len(skills) - 1}\n"
        infofile += f"🔹 Total Achievments ⊸⊱ {len(achievment) - 1}"
        message.reply_text(
            infofile,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Battle", callback_data=f"battle={user_id}"),
                        InlineKeyboardButton(text="Family", callback_data=f"family={user_id}")
                    ]
                ]
            )
        )
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")
        

def inlinex(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    message.reply_text(
        "Yo1",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="1", callback_data=f"done1"),
                    InlineKeyboardButton(text="2", callback_data=f"done4")
                ]
            ]
        )
    )
"""
def inlinex_callback(update, context):
    query = update.callback_query
    a = 15
    b = 15
    c = a * b
    if query.data == "done1":
        while c > 0:
            c = a * b
            query.message.reply_text(
                f"A = 15\nB = 15\nC = {c}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="3", callback_data="done3"),
                            InlineKeyboardButton(text="2", callback_data="done2")
                        ]
                    ]
                )
            )
        elif query.data == "done2":
            b = b - 2
            c = a * b
            query.message.edit_text(
                f"A = {a} \nB = {b}\nC = {c}"
            )
        elif query.data == "done3":
            b = b - 3
            c = a * b
            query.message.edit_text(
                f"A = {a} \nB = {b}\nC = {c}"
            )
        elif query.data == "done4":
            query.message.edit_text(
                "Cancel",
            )"""
        

DATATYPE_HANDLER = DisableAbleCommandHandler("datatype", datatype, run_async=True)
testdevs1_HANDLER = DisableAbleCommandHandler("testdevs1", testdevs1, run_async=True)
testdevs2_HANDLER = DisableAbleCommandHandler("testdevs2", testdevs2, run_async=True)
INFOOX_HANDLER = DisableAbleCommandHandler("info", infoxx, run_async=True)
inlinex_HANDLER = DisableAbleCommandHandler("inline", inlinex, run_async=True)
#inlinexN_HANDLER = CallbackQueryHandler(inlinex_callback, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)

dispatcher.add_handler(DATATYPE_HANDLER)
dispatcher.add_handler(testdevs1_HANDLER)
dispatcher.add_handler(testdevs2_HANDLER)
dispatcher.add_handler(INFOOX_HANDLER)
dispatcher.add_handler(inlinex_HANDLER)
#dispatcher.add_handler(inlinexN_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
