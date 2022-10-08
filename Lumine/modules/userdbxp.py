import html
from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import ParseMode, MAX_MESSAGE_LENGTH
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from telegram.ext import CallbackContext, CommandHandler, Filters

from Lumine.modules.mongodbtest1 import collection
from Lumine import dispatcher, SUDO_USERS
from Lumine.modules.disable import DisableAbleCommandHandler
from Lumine.modules.helper_funcs.extraction import extract_user



@run_async
def about_bio(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = collection.find({"_id": user.id})

    if info:
        update.effective_message.reply_text("*{}*:\n{}".format(user.first_name, escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text("{} hasn't had a message set about themselves yet!".format(username))
    else:
        update.effective_message.reply_text("You haven't had a bio set about yourself yet!")


__mod_name__ = "DB Func"

GET_BIO_HANDLER = DisableAbleCommandHandler("biox", about_bio, pass_args=True)
dispatcher.add_handler(GET_BIO_HANDLER)
