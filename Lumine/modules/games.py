import html
import random
import time

from telegram import ParseMode, Update, ChatPermissions
from telegram.ext import CallbackContext, run_async
from telegram.error import BadRequest

import Lumine.modules.game_strings as game_strings
from Lumine import dispatcher
from Lumine.modules.disable import DisableAbleCommandHandler
from Lumine.modules.helper_funcs.chat_status import (is_user_admin)
from Lumine.modules.helper_funcs.extraction import extract_user


@run_async
def truth(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(game_strings.TRUTH_STRINGS))


@run_async
def dare(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(game_strings.DARE_STRINGS))


@run_async
def tord(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(game_strings.TORD_STRINGS))



TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)
TORD_HANDLER = DisableAbleCommandHandler("tord", tord)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(TORD_HANDLER)

__mod_name__ = "Games"
__command_list__ = [
   "truth", "dare", "tord",
]

__handlers__ = [
    TRUTH_HANDLER, DARE_HANDLER, TORD_HANDLER,
]
