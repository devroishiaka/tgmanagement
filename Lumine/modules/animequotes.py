import random

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, run_async

import Lumine.modules.animequotesstring as animequotesstring
from Lumine import dispatcher
from Lumine.modules.disable import DisableAbleCommandHandler


def animequotes(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(animequotesstring.ANIMEQUOTES))


def animequotespic(update: Update, context: CallbackContext):
    update.effective_message.reply_photo(random.choice(animequotesstring.QUOTES_IMG))
    

ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("quotes", animequotes, run_async=True)
ANIMEQUOTESPIC_HANDLER = DisableAbleCommandHandler("animequotes", animequotespic, run_async=True)


dispatcher.add_handler(ANIMEQUOTES_HANDLER)
dispatcher.add_handler(ANIMEQUOTESPIC_HANDLER)
