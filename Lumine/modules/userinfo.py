import html
import re
import os
import requests

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html

from Lumine import (
    DEV_USERS,
    OWNER_ID,
    SUDO_USERS,
    SUPPORT_USERS,
    WHITELIST_USERS,
    INFOPIC,
    dispatcher,
    sw,
)
from Lumine.userlist import (SCLASS, ACLASS, BCLASS, CCLASS, DCLASS)
from Lumine.__main__ import STATS, GDPR, TOKEN, USER_INFO
import Lumine.modules.sql.userinfo_sql as sql
from Lumine.modules.disable import DisableAbleCommandHandler
from Lumine.modules.sql.global_bans_sql import is_user_gbanned
from Lumine.modules.sql.afk_sql import is_afk, check_afk_status
from Lumine.modules.sql.users_sql import get_user_num_chats
from Lumine.modules.sql.clear_cmd_sql import get_clearcmd
from Lumine.modules.helper_funcs.chat_status import sudo_plus, gods_plus
from Lumine.modules.helper_funcs.extraction import extract_user
from Lumine.modules.helper_funcs.misc import delete
from Lumine import telethn as LumineTelethonClient, SUDO_USERS, SUPPORT_USERS


def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>Telegram ID</b>\n"
                f"• {html.escape(user2.first_name)}: <code>{user2.id}</code>\n"
                f"• {html.escape(user1.first_name)}: <code>{user1.id}</code>",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s id is <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    else:

        if chat.type == "private":
            msg.reply_text(
                f"Your id is <code>{chat.id}</code>", parse_mode=ParseMode.HTML
            )

        else:
            msg.reply_text(
                f"This group's id is <code>{chat.id}</code>", parse_mode=ParseMode.HTML
            )


@LumineTelethonClient.on(
    events.NewMessage(pattern="/ginfo ", from_users=(SUDO_USERS or []) + (SUPPORT_USERS or []))
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there."
        )
        return
    msg = f"**ID**: `{entity.id}`"
    msg += f"\n**Title**: `{entity.title}`"
    msg += f"\n**Datacenter**: `{entity.photo.dc_id}`"
    msg += f"\n**Video PFP**: `{entity.photo.has_video}`"
    msg += f"\n**Supergroup**: `{entity.megagroup}`"
    msg += f"\n**Restricted**: `{entity.restricted}`"
    msg += f"\n**Scam**: `{entity.scam}`"
    msg += f"\n**Slowmode**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**Username**: {entity.username}"
    msg += "\n\n**Member Stats:**"
    msg += f"\n`Admins:` `{len(totallist)}`"
    msg += f"\n`Users`: `{totallist.total}`"
    msg += "\n\n**Admins List:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**Description**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)


def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")


def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        delmsg = message.reply_text("I can't find a user from this.")

        cleartime = get_clearcmd(chat.id, "info")
        
        if cleartime:
            context.dispatcher.run_async(delete, delmsg, cleartime.time)

        return

    else:
        return

    rep = message.reply_text("<code>Sᴇᴀʀᴄʜɪɴɢ Dᴀᴛᴀʙᴀsᴇ...</code>", parse_mode=ParseMode.HTML)

    text = (
        f"┏━━━•°•━━•°•\n"
        f"┣<b> ⊱ Usᴇʀ Iɴғᴏ ⊰</b>\n┃\n"
        f"┣◈ ID ⊶ <code>{user.id}</code>\n"
        f"┣◈ Fɪʀsᴛ Nᴀᴍᴇ ⊶ {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n┣◈ Lᴀsᴛ Nᴀᴍᴇ ⊶ {html.escape(user.last_name)}"

    if user.username:
        text += f"\n┣◈ UsᴇʀNᴀᴍᴇ ⊶ @{html.escape(user.username)}\n┃"


    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ <b>Dragon GOD</b>"               #Title----s-class------------------------
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ <b>S-Class</b>"
        disaster_level_present = True
    elif user.id in SUDO_USERS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ <b>A-class</b>"
        disaster_level_present = True
    elif user.id in SUPPORT_USERS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ <b>B-class</b>"
        disaster_level_present = True
    elif user.id in WHITELIST_USERS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ <b>C-Class</b>"
        disaster_level_present = True
    elif user.id in SCLASS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ S-Class"
        disaster_level_present = True
    elif user.id in ACLASS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ A-Class"
        disaster_level_present = True
    elif user.id in BCLASS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ B-Class"
        disaster_level_present = True
    elif user.id in CCLASS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ C-Class"
        disaster_level_present = True
    elif user.id in DCLASS:
        text += "\n┣━◈ Rᴀɴᴋ ⊶ D-Class"
        disaster_level_present = True

    # if disaster_level_present:
    #     text += ' [<a href="https://t.me/OnePunchUpdates/155">?</a>]'.format(
    #         bot.username)

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}"
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n┣━◈ Tɪᴛʟᴇ ⊶ <b>{custom_title}</b>"    #Title---dragon-slayer------------------------
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n┃\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            _file = bot.get_file(profile["file_id"])
            _file.download(f"{user.id}.png")

            delmsg = message.reply_document(
                document=open(f"{user.id}.png", "rb"),
                caption=(text),
                parse_mode=ParseMode.HTML,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            delmsg = message.reply_text(
                text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

    else:
        delmsg = message.reply_text(
            text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )

    rep.delete()


    cleartime = get_clearcmd(chat.id, "info")
    
    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)


def about_me(update: Update, context: CallbackContext):  #guilds-------------------------------
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*Guild*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"`{username} hasn't registered yet!`"
        )
    else:
        update.effective_message.reply_text("You not part of any guild 👀,\nPlease join a guild or create one")


def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("Error! Unauthorized")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("Authorized...Information updated!")
            elif user_id == bot.id:
                message.reply_text("Request completed")
            else:
                message.reply_text("successfully DONE!")
        else:
            message.reply_text(
                "The guild name needs to be under {} characters! You have {}.".format(
                    MAX_MESSAGE_LENGTH // 4, len(info[1])
                )
            )


@sudo_plus
def stats(update: Update, context: CallbackContext):
    stats = "<b>📊 Current stats:</b>\n" + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(result, parse_mode=ParseMode.HTML)


def about_bio(update: Update, context: CallbackContext):       #points----------------------------
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*Points*:\n{}".format(escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} is not registered"
        )
    else:
        update.effective_message.reply_text(
            "You haven't yet registered!👀"
        )

@gods_plus
def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "Ha, you can't set your own points! You're at the mercy of gods here..."
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("You are not authorised")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "Erm... yeah, I only trust Dragon god."
            )
            return

        text = message.text
        bio = text.split(
            None, 1
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "Updated {}'s points!".format(repl_message.from_user.first_name)
                )
            else:
                message.reply_text(
                    "points needs to be under {} characters! You tried to set {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])
                    )
                )
    else:
        message.reply_text("Reply to someone to set their points!")


def gdpr(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Deleting identifiable data...")
    for mod in GDPR:
        mod.__gdpr__(update.effective_user.id)

    update.effective_message.reply_text("Your personal data has been deleted.\n\nNote that this will not unban "
                                        "you from chats if you are banned, as that is telegram data, not Eri's data. "
                                        "Flooding, warns, and gbans are also preserved, as of "
                                        "[this](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/), "
                                        "which clearly states that the right to erasure does not apply "
                                        "\"for the performance of a task carried out in the public interest\", as is "
                                        "the case for the aforementioned pieces of data.",
                                        parse_mode=ParseMode.MARKDOWN)


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"┣━◈<b> Gᴜɪʟᴅ ⊶ </b>{me}\n"
    if bio:
        result += f"┣━◈<b> Pᴏɪɴᴛs ⊶ </b>{bio}"
    result = result.strip("")
    return result

"""
def __user_info__(user_id):
    is_blacklisted = sql.is_user_blacklisted(user_id)

    text = "┣◈BʟᴀcᴋWɪzᴀʀᴅ ⊶ <b>{}</b>"
    if user_id in [777000, 1087968824]:
        return ""
    if user_id == dispatcher.bot.id:
        return "OFC NO"
    if int(user_id) in SUDO_USERS:
        return ""
    if is_blacklisted:
        text = text.format("Yes")
        reason = sql.get_reason(user_id)
        if reason:
            text += f"\nReason: <code>{reason}</code>"
    else:
        text = text.format("No")

    return text
"""

def __gdpr__(user_id):
    sql.clear_user_info(user_id)
    sql.clear_user_bio(user_id)



SET_BIO_HANDLER = DisableAbleCommandHandler("setpointsxx", set_about_bio, run_async=True)
GET_BIO_HANDLER = DisableAbleCommandHandler("pointsxx", about_bio)

STATS_HANDLER = CommandHandler("stats", stats, run_async=True)
ID_HANDLER = DisableAbleCommandHandler("id", get_id, run_async=True)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid, run_async=True)
INFO_HANDLER = DisableAbleCommandHandler(("infoxx", "book"), info, run_async=True)
GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.chat_type.private, run_async=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler(("joinxx", "createxx"), set_about_me, run_async=True)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("myguildxx", about_me, run_async=True)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(GDPR_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "Info"
__command_list__ = ["ksetpoint", "pointsxx", "join", "Myguild", "info", "gprd"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    GDPR_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
