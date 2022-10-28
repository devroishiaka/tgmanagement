import json
import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, CallbackQueryHandler, run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import dispatcher
from Lumine.modules.helper_funcs.extraction import extract_user


def help1(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(
        "Please choose for testing:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Yes", callback_data="yess_"),
                    InlineKeyboardButton(text="Noo", callback_data="nooo_")
                ],
                [
                    InlineKeyboardButton(text="Maybe", callback_data="maybe_"),
                    InlineKeyboardButton(text="Abs No", callback_data="absno_")
                ]
            ]
        ),
        parse_mode=ParseMode.HTML,
    )

def help1btn_callback(update: Update, context: CallbackContext):
    message = update.effective_message
    query = update.callback_query
    if query.data == "yess_":
        query.message.edit_text(
            "hello, your answer- Yes"
        )
    elif query.data == "nooo_":
        query.message.edit_text(
            "hello, your answer- Noo"
        )


def help11(update: Update, context: CallbackContext):
    message = update.effective_message
    if message.reply_to_message:
        message.reply_text(
            "choose:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Yes", callback_data="Yes111_"),
                        InlineKeyboardButton(text="No", callback_data="Noo111_")
                    ]
                ]
            )
        )
    else:
        message.reply_text("Hmm, please reply")

def help11btn_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.effective_message
    if query.data == "Yes111_":
        query.message.edit_text("hmm yes")
    elif query.data == "Noo111_":
        query.message.edit_text("hmm noo")



HELP_1_HANDLER = CommandHandler("help1", help1, run_async=True)
HELP_1_BTN_HANDLER = CallbackQueryHandler(help1btn_callback)
HELP11_HANDLER = CommandHandler("friend", help11, run_async=True)
HELP11_BTN_HANDLER = CallbackQueryHandler(help11btn_callback)


dispatcher.add_handler(HELP_1_HANDLER)
dispatcher.add_handler(HELP_1_BTN_HANDLER)
dispatcher.add_handler(HELP11_HANDLER)
dispatcher.add_handler(HELP11_BTN_HANDLER)

