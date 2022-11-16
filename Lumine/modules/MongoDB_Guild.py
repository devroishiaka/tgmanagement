import asyncio
from datetime import datetime
from asyncio import sleep
from telethon import events
from Lumine import telethn as LumineTelethonClient

from Lumine.modules.MongoDB import collection1, collection2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import MAX_MESSAGE_LENGTH, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import (
    dispatcher
)
from Lumine.modules.helper_funcs.alternate import typing_action
from Lumine.modules.helper_funcs.chat_status import sudo_plus, gods_plus
from Lumine.modules.helper_funcs.extraction import extract_user
from Lumine.modules.disable import DisableAbleCommandHandler

#/join <guild name>
@LumineTelethonClient.on(events.NewMessage(pattern="(?i)/join"))
async def joinx(event):
    sender = await event.get_sender()
    list_of_words = event.message.text.split(" ")
    if len(list_of_words) > 1:
        guild = list_of_words[1]
        registerd = collection1.find_one({"_id": sender.id})
        if registerd:
            guild_exist = collection2.find({"Guild_Name": guild})
            if guild_exist:
                collection2.update_one({"Guild_Name": guild}, {"$inc":{"Members": 1}})
                collection1.update_one({"_id": sender.id}, {"$set":{"Status": guild}})
                return await event.respond(
                f"━━━━━━━━━━━━━━━━\n\n🎉 {sender.first_name} Successfully joined the {guild} guild!!!\n━━━━━━━━━━━━━━━━"
                )
            else:
                return await event.respond(
                f"{guild} guild doesn’t exist!!"
                )
        else:
            return await event.respond(
            "You not registerd!!\nUse /register to get registerd in this game"
            )
    else:
        return await event.respond("Wrong format, use this way:\n/join <Guild Name>")



#/deposit <amount>
def depositx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    sender_id = int(sender_id)
    sender_name = update.effective_user.first_name
    bot = context.bot
    list_of_words = message.text.split(" ")
    if len(list_of_words) > 1:
        points1 = int(list_of_words[1])
        registerd = collection1.find_one({"_id": sender_id})
        if registerd:
            result1 = int(registerd["Points"])
            result2 = registerd["Status"]
            if result2 == "No":
                message.reply_text("Brooooooooooo,\nJoin a guild first to have a vault")
            else :
                if points1 < result1:
                    collection2.update_one({"Guild_Name": result2}, {"$inc": {"Vault": points1}})
                    points = 0-points1
                    collection1.update_one({"_id": sender_id}, {"$inc": {"Points": points, "Deposit": points1, "TDeposit": points1}})
                    message.reply_text(f"💸 {sender_name} Successfully Deposited the points!")
                else:
                    message.reply_text("you dont have enough points to deposit")
        else:
            message.reply_text("You not registerd!!\nUse /register to get registerd in this game")
    else:
        message.reply_text("Provide me something to deposit\nCorrect Format: /deposit <amount>")

        
#/guild or /guild <guild name>
def guildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    list_of_words = message.text.split(" ")
    bot = context.bot
    chat_id = update.effective_chat.id
    if len(list_of_words) == 1:
        sender_id = int(sender_id)
        registerd = collection1({"_id": sender_id})
        if registerd:
            guild_exist = registerd["Status"]
            if guild_exist != "No":
                guild = collection2.find_one({"Guild_Name": guild_exist})

                gname = results["Guild_FName"]
                grank = results["Guild_Rank"]
                glevel = results["Guild_Level"]
                gcreator = results["Guild_Creator"]
                gvault = results["Vault"]
                gmembers = results["Members"]
                gcrime = results["Crime_Rate"]
                final = f"""
━━━━━━━━━҉━━━━━━━━━
<b>⊱ {gname} ⊰</b>

◈ Guild Name = <code>{guild_name}</code>
◈ Creator = <code>{gcreator}</code>
◈ Rank = <code>{grank}</code>
◈ Level = <code>{glevel}</code>
◈ Members = <code>{gmembers}</code>
◈ Vault = <code>{gvault}</code>
◈ Crime Rate = <code>{gcrime}</code>
━━━━━━━━━҉━━━━━━━━━
"""

                pfp = results["Guild_Pfp"]
                if pfp == "No":
                    bot.send_message(
                        chat_id,
                        final,
                        parse_mode=ParseMode.HTML
                    )
                else:
                    boot.send_photo(
                        chat_id,
                        pfp,
                        caption=final,
                        parse_mode=ParseMode.HTML
                    )
            else:
                message.reply_text("No Such Guild Found")
        else:
            message.reply_text("You not registerd!!\nUse /register to get registerd in this game")
    else:
        message.reply_text("LOL")           



def vault(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    user_id = int(user_id)
    registerd = collection1.find_one({"_id": user_id})
    if registerd:
        guild_exist = registerd["Status"]
        if guild_exist == "No":
            message.reply_text("Join a guild first to have a Guild Vault")
        else:
            guild = collection2.find_one({"Guild_Name": guild_exist})
            guild_fname = guild["Guild_FName"]
            msg_final = f"━━━━━━━━━҉━━━━━━━━━\n<b>⊱ {guild_fname} ⊰</b>\n\n"
            alluser = collection1.find({"Status": guild_exist})
            amount = int(guild["Vault"])
            msg_final += f"{guild_exist} Have a total amount of {amount} in the vault\n"
            creator = guild["Guild_Creator"]
            msg_final += f"The Creator of this Guild is {creator}"
            msg_final += "\n━━━━━━━━━҉━━━━━━━━━\n"
            msg_final += "Members of the guild have contributed and have deposited thier points in the vault\n\n"
            msg_final += "The Members LIst are listed below:\n"
            msg_final += f"<a href='t.me/Kazumaclanxd'>Kᴀᴢᴜᴍᴀ Cʟᴀɴ</a> • 1000\n"
            for users in alluser:
                deposit = int(users["Deposit"])
                if deposit != 0:
                    uname = users["Name"]
                    userid = users["_id"]
                    msg_final += f"<a href='tg://user?id={userid}'>{uname}</a>"
                    msg_final += " • "
                    msg_final += f"<code>{deposit}</code>"
                    msg_final += "\n"
                else:
                    continue
            message.reply_text(msg_final, parse_mode=ParseMode.HTML)
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game.")


def allguild(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    allguild = collection2.find().sort("Guild_Level",-1).limit(10)
    final = "━━━━━━━━━҉━━━━━━━━━\n<b>Top Guilds</b> 🌐\n\nGuild Name • Level\n"
    for result in allguild:
        final += result["Guild_Name"]
        final += " • "
        levels = str(result["Guild_Level"])
        final += f"<code>{levels}</code>"
        final += "\n"
    message.reply_text(final, parse_mode=ParseMode.HTML)


def leavex(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    registerd = collection1.find_one({"_id": sender_id})
    if registerd:
        guild_exist = str(registerd["Status"])
        if guild_exist != "No":
            message.reply_text(
                "YOU SURE THAT YOU WANT TO LEAVE THIS GUILD ?",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="YES ✅", callback_data=f"leave={sender_id}"),
                            InlineKeyboardButton(text="NO ❌", callback_data=f"dell={sender_id}")
                        ]
                    ]
                )
            )
        else:
            message.reply_text("join a guild first to leave that guild")
    else:
        message.reply_text("You not registerd!!\nUse /register to get registerd in this game.")


def leavex_btn(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    userid = update.effective_user.id
    user_id = int(userid)
    query_id = query.id
    splitter = query.data.split("=")
    query_match = splitter[0]
    if query_match != "dell":
        senderid = splitter[1]
        sender_id = int(senderid)
        if user_id == sender_id:
            guild_name1 = collection1.find_one({"_id": sender_id})
            guild_name = guild_name1["Status"]
            collection2.update_one({"Guild_Name": guild_name}, {"$inc": {"Members": -1}})
            collection1.update_one({"_id": sender_id}, {"$set": {"Status": "No", "Deposit": 0}})
            query.message.edit_text("✅ You successfully left the guild!!!")
        else:
            bot.answer_callback_query(query_id, text="WHO ARE YOU ???")
    else:
        sender_id = splitter[1]
        senderid = int(sender_id)
        if user_id == senderid:
            query.message.delete()
        else:
            bot.answer_callback_query(query.id, text="WHO ARE YOU ???")
            


DEPOSITX_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)
GUILD_HANDLER = DisableAbleCommandHandler("guild", guildx, run_async=True)
VAULT_HANDLER = DisableAbleCommandHandler("vault", vault, run_async=True)
TOPGUILDS_HANDLER = DisableAbleCommandHandler("topguilds", allguild, run_async=True)
LEAVEX_HANDLER = DisableAbleCommandHandler("leave", leavex, run_async=True)
LEAVEX_BTN_HANDLER = CallbackQueryHandler(leavex_btn, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)

dispatcher.add_handler(DEPOSITX_HANDLER)
dispatcher.add_handler(GUILD_HANDLER)
dispatcher.add_handler(VAULT_HANDLER)
dispatcher.add_handler(TOPGUILDS_HANDLER)
dispatcher.add_handler(LEAVEX_HANDLER)
dispatcher.add_handler(LEAVEX_BTN_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
