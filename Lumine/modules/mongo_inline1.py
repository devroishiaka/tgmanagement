
import json
import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, CallbackQueryHandler, run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import dispatcher
from Lumine.modules.helper_funcs.extraction import extract_user


def help222(update: Update, context: CallbackContext):
    message = update.effective_message
    if message.reply_to_message:
        message.reply_text(
            "choose:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Yes", callback_data="222_"),
                        InlineKeyboardButton(text="No", callback_data="333_")
                    ]
                ]
            )
        )
    else:
        message.reply_text("Hmm, please reply")

def help22btn_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.effective_message
    if query.data == "222_":
        query.message.edit_text("hmm yes")
    elif query.data == "333_":
        query.message.edit_text("hmm noo")

HELP11_HANDLER = CommandHandler("hmmm", help222, run_async=True)
HELP11_BTN_HANDLER = CallbackQueryHandler(help22btn_callback)

dispatcher.add_handler(HELP11_HANDLER)
  dispatcher.add_handler(HELP11_BTN_HANDLER)
