import html
import os
from typing import Optional

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
from Lumine.modules.log_channel import gloggable
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

@gloggable
def registerx(update: Update, context: CallbackContext) -> str:
    reply = check_user_id(user_id, bot)
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    update.effective_message.reply_text("Your request has been successfully sent to the ministry...\nPlease wait till they approve your request")
    
    log_message = (
        f"#REGISTRATION\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


def godslist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    true_god = list(set(GODS))
    msg = "<b>Gods - :</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            msg += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    message.reply_text(msg, parse_mode=ParseMode.HTML)




#=======[]=========[]=======[]======[]============[]==========[]===========[]==========[]=========[]=========[]=====[]
REGISTERX_HANDLER = CommandHandler(("register"), registerx, run_async=True)
GODSLIST_HANDLER = CommandHandler(("godslist"), godslist, run_async=True)



dispatcher.add_handler(REGISTERX_HANDLER)
dispatcher.add_handler(GODSLIST_HANDLER)



__handlers__ = [REGISTERX_HANDLER]
