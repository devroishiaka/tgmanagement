
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
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        message.reply_text(
            "choose:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✅️", callback_data=f"yes={user_id}"),
                        InlineKeyboardButton(text="❌", callback_data="no_")
                    ]
                ]
            )
        )
    else:
        message.reply_text("Please reply to someone!!")

def help22btn_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.effective_message
    sender_id = update.effective_user.id
    splitter = query.data.split("=")
    query_match = splitter[0]
    if query_match == "yes":
        user_id = splitter[1]
        query.message.edit_text(f"hmm yes {sender_id} , {user_id}")
    elif query.data == "no_":
        query.message.edit_text("hmm noo")

HELP11_HANDLER = CommandHandler("hmmm", help222, run_async=True)
HELP11_BTN_HANDLER = CallbackQueryHandler(help22btn_callback)

dispatcher.add_handler(HELP11_HANDLER)
dispatcher.add_handler(HELP11_BTN_HANDLER)
