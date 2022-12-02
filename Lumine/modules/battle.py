import json
import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, CallbackQueryHandler, run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import dispatcher
from Lumine.modules.helper_funcs.extraction import extract_user

"""
B = Battle(YES or NO)
BA = Battle attack(weapons of the attacker)
BD = Battle defence(weapons of the defender)
"""

def battleff(update: Update, context: CallbackContext):
    message = update.effective_message
    attacker_id = update.effective_user.id
    attacker_id= int(attacker_id)
    message.reply_text(
        "CHOOSE",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="YES", callback_data=f"Byes={attacker_id}"),
                    InlineKeyboardButton(text="NOO", callback_data=f"Bnoo={attacker_id}")
                ]
            ]
        )
    )


def battle_but1(update: Update, context: CallbackContext):
    query = update.callback_query
    splitter = query.data.split("=")
    if "Byes" in splitter:
        attacker_id = splitter[1]
        query.message.edit_text(
            "Battle weapons (attacker)",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data=f"BA1={attacker_id}"),
                        InlineKeyboardButton(text="2", callback_data=f"BA2={attacker_id}"),
                        InlineKeyboardButton(text="3", callback_data=f"BA3={attacker_id}"),
                        InlineKeyboardButton(text="4", callback_data=f"BA4={attacker_id}"),
                    ]
                ]
            )
        )
    else:
        query.message.edit_text(
            "LOL"
        )

def battle_but2(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    splitter = query.data.split("=")
    c = 20
    while c > 0:
        if "BA1" in splitter:
            c = c - 1
            query.message.edit_text(
                f"{c}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="1", callback_data=f"BA1={attacker_id}"),
                            InlineKeyboardButton(text="2", callback_data=f"BA2={attacker_id}"),
                            InlineKeyboardButton(text="3", callback_data=f"BA3={attacker_id}"),
                            InlineKeyboardButton(text="4", callback_data=f"BA4={attacker_id}"),
                        ]
                    ]
                )
            )
        elif "BA2" in splitter:
            c = c - 2
            query.message.edit_text(
                f"{c}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="1", callback_data=f"BA1={attacker_id}"),
                            InlineKeyboardButton(text="2", callback_data=f"BA2={attacker_id}"),
                            InlineKeyboardButton(text="3", callback_data=f"BA3={attacker_id}"),
                            InlineKeyboardButton(text="4", callback_data=f"BA4={attacker_id}"),
                        ]
                    ]
                )
            )
        elif "BA3" in splitter:
            c = c - 3
            query.message.edit_text(
                f"{c}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="1", callback_data=f"BA1={attacker_id}"),
                            InlineKeyboardButton(text="2", callback_data=f"BA2={attacker_id}"),
                            InlineKeyboardButton(text="3", callback_data=f"BA3={attacker_id}"),
                            InlineKeyboardButton(text="4", callback_data=f"BA4={attacker_id}"),
                        ]
                    ]
                )
            )
        elif "BA4" in splitter:
            c = c - 4
            query.message.edit_text(
                f"{c}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="1", callback_data=f"BA1={attacker_id}"),
                            InlineKeyboardButton(text="2", callback_data=f"BA2={attacker_id}"),
                            InlineKeyboardButton(text="3", callback_data=f"BA3={attacker_id}"),
                            InlineKeyboardButton(text="4", callback_data=f"BA4={attacker_id}"),
                        ]
                    ]
                )
            )

battleff_handler = CommandHandler("battlee", battleff)
button1_callback_handler = CallbackQueryHandler(battle_but1, pattern=r"Byes")
button2_callback_handler = CallbackQueryHandler(battle_but2, pattern=r"BA")

dispatcher.add_handler(battleff_handler)
dispatcher.add_handler(button1_callback_handler)
dispatcher.add_handler(button2_callback_handler)
