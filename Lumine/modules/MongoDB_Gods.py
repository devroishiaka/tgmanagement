
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

#/create <guild name>
@gods_plus
def createguildx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    text = message.text
    if len(text) == 2:
        message.reply_text("Correct format:\n/create <user ID> <Guild Name>")
    elif len(text) > 2:
        splitter = text.split(None, 1)[1]
        guild_id = splitter.split(" ")[0]
        guild_name = splitter.split(None, 1)[1]

        collection2.insert_one({"_id": guild_id, "Guild_Name": guild_name, "Guild_FName": guild_name, "Guild_Level": 1, "Members": 1, "Vault": 2000, "Guild_Creator": "Gods", "Crime_Rate": 0, "Guild_Rank": 1, "Guild_Status": "No", "Guild_Pfp": "No" })
        collection1.update_one({"_id": guild_id}, {"$inc": {"Points": -1000}})
        message.reply_text("✅ Created a new guild!")
    else:
        message.reply_text("Correct format:\n/create <user ID> <Guild Name>")



#/setpoints
@gods_plus
def setpointsx(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot
    list_of_words = message.text.split(" ")
    
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        point1 = list_of_words[1]
        points1 = int(point1)
        collection1.update_one({"_id": user_id}, {"$inc": {"Points": points1}})
        message.reply_text("✅ successfully updated the points")
        
    if len(list_of_words) == 3:
        id_tag = list_of_words[1]
        point2 = list_of_words[2]
        points2 = int(point2)
        collection1.update_one({"_id": id_tag}, {"$inc": {"Points": points2}})
        message.reply_text("✅ successfully updated the points")
        
    elif len(list_of_words) == 2:
        point3 = list_of_words[1]
        points3 = int(point3)
        collection1.update_one({"_id": sender_id}, {"$inc": {"Points": points3}})
        message.reply_text("✅ successfully updated the points")


#/setowner
@gods_plus
def setowner(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    text = message.text
    splitter = text.split(
        None, 1
    )
    user_id = splitter[1]
    results = collection1.find_one({"_id": user_id})
    result = results["Name"]
    collection2.update_one({"_id": user_id}, {"$set": {"Guild_Creator": result}})
    message.reply_text("✅ successfully updated The Guild INFO")

    
@gods_plus
def checkdata(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    text = message.text
    if len(text) > 1:
        splitter = text.split(
            None, 1
        )
        user_id = splitter[1]
        results = collection1.find_one({"_id": user_id})
        if results:
            name = results["Name"]
            level = results["Level"]
            rank = results["Rank"]
            points = results["Points"]
            gender = results["Gender"]
            partner = results["Partner"]
            friend = results["Friend"]
            father = results["Father"]
            mother = results["Mother"]
            children = results["Children"]
            bounty = results["Bounty"]
            status = results["Status"]

            message.reply_text(f"""
━━━━━━━━━҉━━━━━━━━━
<b>USERDATA</b>

USER ID = <code>{user_id}</code>
USER NAME = <code>{name}</code>
LEVEL = <code>{level}</code>
RANK = <code>{rank}</code>
POINTS = <code>{points}</code>
GENDER = <code>{gender}</code>
FRIEND = <code>{friend}</code>
PARTNER = <code>{partner}</code>
FATHER = <code>{father}</code>
MOTHER = <code>{mother}</code>
CHILDREN = <code>{children}</code>
BOUNTY = <code>{bounty}</code>
GUILD = <code>{status}</code>
━━━━━━━━━҉━━━━━━━━━
""",
                parse_mode=parse_mode.HTML
            )
        else:
            message.reply_text("NO such user in my Database")
    else:
        message.reply_text("Wrong format\nUse this way /checkdata <user ID>")
       


@gods_plus
def addpfp(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text
    splitter = text.split(
        None, 1
    )
    datatext = splitter[1]
    guild_name = datatext.split(" ")[0]
    pfplink = datatext.split(" ")[1]
    results = collection2.find_one({"Guild_Name": guild_name})
    if results:
        collection2.update_one({"Guild_Name": guild_name}, {"$set": {"Guild_Pfp": pfplink}})
        message.reply_text("✅ Successfully updated the Guild Profile Pic")
    else:
        message.reply_text("NO such GUILD found!!")
        
        

SETPOINTS_HANDLER = DisableAbleCommandHandler("setpoints", setpointsx, run_async=True)
CREATEGUILD_HANDLER = DisableAbleCommandHandler("create", createguildx, run_async=True)
SETOWNER_HANDLER = DisableAbleCommandHandler("setowner", setownerx, run_async=True)
CHECKDATA_HANDLER = DisableAbleCommandHandler("checkdata", checkdata, run_async=True)
ADDPFP_HANDLER = DisableAbleCommandHandler("addpfp", addpfp, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)

dispatcher.add_handler(SETPOINTS_HANDLER)
dispatcher.add_handler(CREATEGUILD_HANDLER)
dispatcher.add_handler(SETOWNER_HANDLER)
dispatcher.add_handler(CHECKDATA_HANDLER)
dispatcher.add_handler(ADDPFP_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
