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

#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def joinx(event):
    sender = await event.get_sender()
    list_of_words = event.message.text.split(" ")
    guild = list_of_words[1]
    registerd = collection1.find_one({"_id": sender.id})
    if registerd:
        guild_exist = collection2.find({"Guild_Name": guild})
        if guild_exist:
            collection2.update_one({"Guild_Name": guild}, {"$inc":{"Members": 1}})
            collection1.update_one({"_id": sender.id}, {"$set":{"Status": guild}})
            return await event.respond(
            f"🎉 You Successfully joined the {guild} guild!!!"
            )
        else:
            return await event.respond(
            f"{guild} guild dont exist!!"
            )
    else:
        return await event.respond(
        "You not registerd!!\nUse /register to get registerd in this game"
        )



#/deposit <amount>
def depositx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    points1 = int(list_of_words[1])
    points = 0-points1
    registerd = collection.find_one({"_id": sender_id})
    if registerd:
        if len(list_of_words) == 2:
            results1 = collection.find_one({"_id": sender_id})
            result1 = int(results["Points"])
            result2 = str(results["Status"])
            if result2 == "No":
                message.reply_text("Brooooooooooo,\nJoin a guild first to have a vault")
            else :
                if points < result1:
                    collection2.update_one({"Guild_Name": result2}, {"$inc": {"Vault": points}})
                    collection1.update_one({"_id": sender_id}, {"$inc": {"Points": points}})
                    message.reply_text("💸 Successfully Deposited the points!")
                else:
                    message.reply_text("you dont have enough points to deposit")
        else:
            message.reply_text("Provide me something to deposit")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game")


DEPOSITX_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)

dispatcher.add_handler(DEPOSITX_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
