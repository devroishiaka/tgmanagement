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
        parse_mode=ParseMode.MARKDOWN,
    )

def help1btn_callback(update: Update, context: CallbackContext):
    message = update.effective_message
    query = update.callback_query
    if query.data == "yess_":
        query.message.reply_text(
            "hello, your answer- Yes"
        )
    elif query.data == "nooo_":
        query.message.reply_text(
            "hello, your answer- Noo"
        )
    elif query.data == "maybe_":
        query.message.reply_text(
            "hello, your answer- Maybe"
        )
    else query.data == "absno_":
        query.message.reply_text(
            "hello, your answer- Abs No"
        )


HELP_1_HANDLER = DisableAbleCommandHandler("help1", help1, run_async=True)
HELP_1_BTN_HANDLER = CallbackQueryHandler(help1btn_callback, pattern=r"yess_", run_async=True)

dispatcher.add_handler(HELP_1_HANDLER)
dispatcher.add_handler(HELP_1_BTN_HANDLER)
