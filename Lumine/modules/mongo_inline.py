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


def friendx(update: Update, context: CallbackContext):
    message = update.effective_message
    if message.reply_to_message:
        message.reply_text(
            "Do you agree?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Yes", callback_data="yessx_"),
                        InlineKeyboardButton(text="No", callback_data="nooox_")
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        message.reply_text("lol, reply please")


def friendbtn_callback(update: Update, context: CallbackContext):
    message = update.effective_message
    query = update.callback_query
    if query.data == "yessx_":
        query.message.edit_text(
            "Congratulations🎊"
        )
    elif query.data == "nooox_":
        query.message.edit_text(
            "Congratulations🎊"
        )




HELP_1_HANDLER = CommandHandler("help1", help1, run_async=True)
HELP_1_BTN_HANDLER = CallbackQueryHandler(help1btn_callback)
FRIENDSX_HANDLER = CommandHandler("addfriend", friendx, run_async=True)
FRIENDSX_BTN_HANDLER = CallbackQueryHandler(friendbtn_callback)

dispatcher.add_handler(HELP_1_HANDLER)
dispatcher.add_handler(HELP_1_BTN_HANDLER)
dispatcher.add_handler(FRIENDSX_HANDLER)
dispatcher.add_handler(FRIENDSX_BTN_HANDLER)
