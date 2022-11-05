
import json
import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, CallbackQueryHandler, run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import dispatcher
from Lumine.modules.helper_funcs.extraction import extract_user


def bann(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    bot = context.bot
    args = context.args
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        useridd = int(user_id)
        bot.sendMessage(
            chat.id,
            text = "Choose",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="✅", callback_data=f"unbanb_unban={useridd}"
                        ),
                        InlineKeyboardButton(text="❌", callback_data="unbanb_del"),
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML,
        )

def unbanb_btn(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    query = update.callback_query
    chat = update.effective_chat
    user = update.effective_user
    senderid = update.effective_user.id
    if query.data != "unbanb_del":
        splitter = query.data.split("=")
        query_match = splitter[0]
        if query_match == "unbanb_unban":
            user_id = splitter[1]
            user_id = int(user_id)
            if user_id == senderid:
                bot.answer_callback_query(
                    query.id,
                    text="You don't have enough rights",
                    show_alert=True,
                )
            elif user_id != senderid:
                bot.answer_callback_query(query.id, text="congo!!!")
            
    else:
        query.message.delete()
        bot.answer_callback_query(query.id, text="Deleted!")

HELP11_HANDLER = CommandHandler("hmm", bann, run_async=True)
HELP11_BTN_HANDLER = CallbackQueryHandler(unbanb_btn)

dispatcher.add_handler(HELP11_HANDLER)
dispatcher.add_handler(HELP11_BTN_HANDLER)
