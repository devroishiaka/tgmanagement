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
    if len(list_of_words) > 1:
        guild = list_of_words[1]
        registerd = collection1.find_one({"_id": sender.id})
        if registerd:
            guild_exist = collection2.find({"Guild_Name": guild})
            if guild_exist:
                collection2.update_one({"Guild_Name": guild}, {"$inc":{"Members": 1}})
                collection1.update_one({"_id": sender.id}, {"$set":{"Status": guild}})
                return await event.respond(
                f"━━━━━━━━━━━━━━\n🎉 {sender.first_name} You Successfully joined the {guild} guild!!!\n━━━━━━━━━━━━━━"
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
    bot = context.bot
    list_of_words = message.text.split(" ")
    if len(list_of_words) > 1:
        points1 = int(list_of_words[1])
        registerd = collection1.find_one({"_id": sender_id})
        if registerd:
            result1 = int(registerd["Points"])
            result2 = str(registerd["Status"])
            if result2 == "No":
                message.reply_text("Brooooooooooo,\nJoin a guild first to have a vault")
            else :
                if points1 < result1:
                    collection2.update_one({"Guild_Name": result2}, {"$inc": {"Vault": points1}})
                    points = 0-points1
                    collection1.update_one({"_id": sender_id}, {"$inc": {"Points": points, "Deposit": points1}})
                    message.reply_text("💸 Successfully Deposited the points!")
                else:
                    message.reply_text("you dont have enough points to deposit")
        else:
            message.reply_text("You not registerd!!\nUse /register to get registerd in this game")
    else:
        message.reply_text("Provide me something to deposit\nCorrect Format: /deposit <amount>")

        
#/guild or /guild <guild name>
def guild(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text
    splitter = text.split(" ")
    if len(splitter) > 1:
        guild_name = text.split(None, 1)[1]
        results = collection2.find_one({"Guild_Name": guild_name})
        if results:
            gname = results["Guild_FName"]
            grank = results["Guild_Rank"]
            glevel = results["Guild_Level"]
            gcreator = results["Guild_Creator"]
            gvault = results["Vault"]
            gmembers = results["Members"]
            gcrime = results["Crime_Rate"]

            pfp = results["Guild_Pfp"]
            if pfp == "NO":
                message.reply_text(f"""
━━━━━━━҉━━━━━━━
<b>⊱ {gname} ⊰</b>

◈ Guild Name = <code>{guild_name}</code>
◈ Creator = <code>{gcreator}</code>
◈ Rank = <code>{grank}</code>
◈ Level = <code>{glevel}</code>
◈ Members = <code>{gmembers}</code>
◈ Vault = <code>{gvault}</code>
◈ Crime Rate = <code>{gcrime}</code>
━━━━━━━҉━━━━━━━
""",
                    parse_mode=ParseMode.HTML,
                )
            else:
                message.reply_photo(pfp, caption=f"""
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
""",
                    parse_mode=ParseMode.HTML,
                )
        else:
            message.reply_text("No Such GUILD found")
    else:
        user_id = update.effective_user.id
        registerd = collection1.find_one({"_id": user_id})
        if registerd:
            guild_name = registerd["Status"]
            if guild_name == "No":
                message.reply_text("Join a Guild first to see info about your guild.\nYou can also search other guild with the format /guild <guild name>")
            else:
                results = collection2.find_one({"Guild_Name": guild_name})
                gname = results["Guild_FName"]
                grank = results["Guild_Rank"]
                glevel = results["Guild_Level"]
                gcreator = results["Guild_Creator"]
                gvault = results["Vault"]
                gmembers = results["Members"]
                gcrime = results["Crime_Rate"]

                pfp = results["Guild_Pfp"]
                if pfp == "No":
                    message.reply_text(f"""
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
""",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    message.reply_photo(pfp, caption=f"""
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
""",
                        parse_mode=ParseMode.HTML,
                    )
        else:
            message.reply_text("You not registerd!!\nUse /register to get registerd in this game.")
            
#/vault        
def vault(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id
    registerd = collection1.find_one({"_id": user_id})
    if registerd:
        guild_exist = registerd["Status"]
        if guild_exist == "No":
            message.reply_text("Join a guild first to have a Guild Vault")
        else:
            guild = collection2.find_one({"Guild_Name": guild_exist})
            msg_final = f"━━━━━━━━҉━━━━━━━━\n<b>⊱ {guild_exist} ⊰</b>\n\n"
            alluser = collection1.find({"Status": guild_exist})
            amount = int(guild["Vault"])
            msg_final += f"{guild_exist} Have a total amount of {amount} in the vault\n"
            creator = guild["Guild_Creator"]
            msg_final += f"The Creator of this Guild is {creator}"
            msg_final += "━━━━━━━━҉━━━━━━━━\n"
            msg_final += "Members of the guild have contributed and have deposited thier points in the vault\n\n"
            msg_final += "The Members LIst are listed below:\n"
            msg_final += f"<a href='t.me/Kazumaclanxd'>KaZuma CLan</a> • 1000\n"
            for users in alluser:
                depositss = users["Deposit"]
                if depositss != 0:
                    uname = users["Name"]
                    userid = users["_id"]
                    msg_final += f"<a href='tg://user?id={userid}'>{uname}</a>"
                    msg_final += " • "
                    deposit = users["Deposit"]
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
    final = "━━━━━━━━━҉━━━━━━━━━\n<b>Top Guilds</b> 🌐\n\n"
    for result in allguild:
        final += (result["Guild_Name"])
        final += " • "
        pointss = str(result["Guild_Level"])
        final += f"<code>{pointss}</code>"
        final += "\n"
    final += "━━━━━━━━━҉━━━━━━━━━"
    message.reply_text(final, parse_mode=parse_mode.HTML)
    

DEPOSITX_HANDLER = DisableAbleCommandHandler("deposit", depositx, run_async=True)
GUILD_HANDLER = DisableAbleCommandHandler("guild", guild, run_async=True)
VAULT_HANDLER = DisableAbleCommandHandler("vault", vault, run_async=True)
TOPGUILDS_HANDLER = DisableAbleCommandHandler("topguilds", allguild, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)

dispatcher.add_handler(DEPOSITX_HANDLER)
dispatcher.add_handler(GUILD_HANDLER)
dispatcher.add_handler(VAULT_HANDLER)
dispatcher.add_handler(TOPGUILDS_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
