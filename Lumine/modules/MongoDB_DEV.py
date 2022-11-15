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


def devregister(update: Update, context: CallbackContext):
    message = update.effective_message
    list_of_words = message.text.split(" ")
    user_id = int(list_of_words[1])
    name = list_of_words[2]
    post_dict1 = {"_id": user_id, "Name": name, "EXP": 10, "Level": 1, "Rank": "D-Class", "Points": 100, "Gender": "No", "Partner": "No", "Friend": "No", "Father": "No", "Mother": "No", "Children": "No", "Status": "No", "Bounty": 0, "Deposit": 0, "TDeposit": 0}
    collection1.insert_one(post_dict1)
    message.reply_text(f"#Terminal\n<code>Operator Command =</code> <b>Register</b>\n<code>Successfully Registered the user</code> <b>{name}</b>", parse_mode=ParseMode.HTML)











DEVREGISTER_HANDLER = DisableAbleCommandHandler("adduser", devregister, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)
#_HANDLER = DisableAbleCommandHandler(, run_async=True)


dispatcher.add_handler(DEVREGISTER_HANDLER)
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
#dispatcher.add_handler()
