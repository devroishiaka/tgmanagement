from telethon import events
from asyncio import sleep

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import telethn as app
from Lumine.modules.helper_funcs.misc import delete


@app.on(events.NewMessage(pattern=f"^[!/]test11 ?(.*)"))
async def friend1(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    sender = await event.get_sender()
    sender_id = sender.id
    await bot.send_message(
        chat_id,
        text="Choose",
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🚫Reject",
                        "reject"
                    ),
                     InlineKeyboardButton(
                        "Done✅",
                        "done"
                    )
                ],
            ]
        )
    )

@app.on_callback_query()
async def callBackButton(bot:Update, callback_query:CallbackQuery):
    data = callback_query.data
    if data == "reject":
        return await callback_query.answer(
            "This request is rejected 💔",
            show_alert = True
        )
    elif data == "done":
        await callback_query.edit_message_text(
            "Donee"
        )
