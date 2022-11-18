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


def devregister(update: Update, context: CallbackContext):
    message = update.effective_message
    list_of_words = message.text.split(" ")
    user_id = int(list_of_words[1])
    name = list_of_words[2]
    post_dict1 = {"_id": sender.id, "Name": name, "EXP": 10, "Level": 1, "Rank": "D-Class", "Points": 100, "Gender": "No", "Partner": "No", "Friend": "No", "Parents": "No", "Parents": "No", "Children": "No", "Status": "No", "Bounty": 0, "Deposit": 0, "TDeposit": 0, "Weapons": ["No"], "WeaSet": [1, 2, 3, 4], "Skills": ["No"], "Health": 100, "DWins": 0, "DTotal": 0, "Invantory": ["No"], "Achievment": ["No"]}
    collection1.insert_one(post_dict1)
    message.reply_text(f"#Terminal\n<code>Operator Command =</code> <b>Register</b>\n<code>Successfully Registered the user</code> <b>{name}</b>", parse_mode=ParseMode.HTML)

def devdelete(update: Update, context: CallbackContext):
    message = update.effective_message
    list_of_words = message.text.split(" ")
    if len(list_of_words) > 1:
        user_id = int(list_of_words[1])
        message.reply_text(
            "Choose the Database",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="User", callback_data=f"db1={user_id}"),
                        InlineKeyboardButton(text="Guild", callback_data=f"db2={user_id}")
                    ]
                ]
            )
        )
    else:
        message.reply_text("use this way\n/deleteone <user ID>")

def delete_callback(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    user = update.effective_user.id
    query_id = query.id
    quser_id = int(user)
    splitter = query.data.split("=")
    user_id = int(splitter[1])
    if quser_id in devlist:
        if splitter[0] == "db1":
            collection1.delete_one({"_id": user_id})
            query.message.edit_text(f"#Terminal\n<code>Operator Command =</code> <b>Delete</b>\n<code>Successfully deleted the user data from the user database</code>", parse_mode=ParseMode.HTML)
        elif splitter[0] == "db2":
            collection2.delete_one({"_id": user_id})
            query.message.edit_text(f"#Terminal\n<code>Operator Command =</code> <b>Delete</b>\n<code>Successfully deleted the user data from the guild database</code>", parse_mode=ParseMode.HTML)
    else:
        bot.answer_callback_query(query_id, text="YOU NOT A DEVELOPER!!!")










DEVREGISTER_HANDLER = DisableAbleCommandHandler("adduser", devregister, run_async=True)
DEVDELETE_HANDLER = DisableAbleCommandHandler("deleteone", devdelete, run_async=True)
DEVDELETE_BTN_HANDLER = CallbackQueryHandler(delete_callback, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)


dispatcher.add_handler(DEVREGISTER_HANDLER)
dispatcher.add_handler(DEVDELETE_HANDLER)
dispatcher.add_handler(DEVDELETE_BTN_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
