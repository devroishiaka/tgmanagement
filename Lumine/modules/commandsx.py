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



def godslist(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    true_god = list(set(GODS))
    msg = "<b>Gods - :</b>\n"
    for each_user in true_god:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            msg += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    message.reply_text(msg, parse_mode=ParseMode.HTML)




#=======[]=========[]=======[]======[]============[]==========[]===========[]==========[]=========[]=========[]=====[]
GODSLIST_HANDLER = CommandHandler(("godslist"), godslist, run_async=True)



dispatcher.add_handler(GODSLIST_HANDLER)


