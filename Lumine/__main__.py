import importlib
import random
import time
import re
from sys import argv
from typing import Optional

from Lumine import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Lumine.modules import ALL_MODULES
from Lumine.modules.helper_funcs.chat_status import is_user_admin
from Lumine.modules.helper_funcs.misc import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
ᏦϴΝΝᏆᏟᎻᏆᏔᎪ !! (◍•ᴗ•◍)

ʜᴏɪ {} sᴀɴ, ɪ’ᴍ Eʀɪ Aᴋᴀɴᴇ, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!! ✨ 
ɪ’ᴍ ᴀ ғᴜɴ ɢᴀᴍᴇ ʙᴏᴛ ᴡɪᴛʜ ғᴀɴᴛᴀsʏ ᴍᴀɢɪᴄᴀʟ ᴛʜᴇᴍᴇ.

ᴛʏᴘᴇ /help ᴛᴏ sᴇᴇ ᴀʟʟ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs

**ɴᴏᴛᴇ**
**ᴄᴜʀʀᴇɴᴛʟʏ ᴛʜɪs ʙᴏᴛ ɪs ɪɴ ɪᴛs ʙᴇᴛᴀ ᴘʜᴀsᴇ. ʏᴏᴜ ᴄᴀɴ’ᴛ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs. ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴡɪᴛʜ ᴛʜᴇ ʙᴏᴛ ɪɴ @friendsdomain**
"""

HELP_STRINGS = """
Hɪ Bᴜᴅᴅy! I'ʍ *Eʀɪ Aᴋᴀɴᴇ*

I'ʍ ᴀ Fun Game ʙᴏᴛ wiᴛh fᴇw fun ᴇxᴛrᴀs! Hᴀvᴇ ᴀ lᴏᴏᴋ ᴀᴛ ᴛhᴇ fᴏllᴏwing fᴏr ᴀn idᴇᴀ ᴏf sᴏʍᴇ ᴏf ᴛhᴇ ᴛhings I ᴄᴀn hᴇlᴩ yᴏu wiᴛh.
"""

HELP_IMG = "https://te.legra.ph/file/847042600ee21d42c79b1.mp4"

ERI_VID= "https://te.legra.ph/file/847042600ee21d42c79b1.mp4",  #start in group vid

ERI_IMG = "https://te.legra.ph/file/7bd18e2d1345f6705f41b.jpg"   #start in pm pic

DONATE_STRING = """ʜᴇʏᴀ, ɢʟᴀᴅ ᴛᴏ ʜᴇᴀʀ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏɴᴀᴛᴇ!
Eʀɪ ɪs ʜᴏsᴛᴇᴅ ᴏɴ ɪᴛs ᴏᴡɴ sᴇʀᴠᴇʀ ᴀɴᴅ ʀᴇϙᴜɪʀᴇ ᴅᴏɴᴀᴛɪᴏɴs. 
ʏᴏᴜ ᴄᴀɴ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ᴡʀɪᴛᴇʀ ᴏғ ᴛʜᴇ ʙᴀsᴇ ᴄᴏᴅᴇ, @Ishikki_Akabane 
ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴊᴏɪɴ ʜɪs ɢʀᴏᴜᴘ ᴛᴏ sᴜᴘᴘᴏʀᴛ ʜɪᴍ.
"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Lumine.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower() == "super_users":
                IMPORTED["super_users"].send_super_users(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_photo(
                ERI_IMG,
                PM_START_TEXT.format(
                    escape_markdown(first_name), escape_markdown(context.bot.first_name)
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Pʟᴀʏ",
                                url="t.me/Friendsdomain".format(
                                    context.bot.username,
                                ),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="Sᴜᴘᴘᴏʀᴛ",
                                url=f"https://t.me/{SUPPORT_CHAT}",
                            ),
                            InlineKeyboardButton(
                                text="Gᴜɪᴅᴇ",
                                callback_data="vegeta_",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                text="kᴀᴢᴜᴍᴀ ᴄʟᴀɴ",
                                url="https://t.me/KazumaclanXD"
                            ),
                            InlineKeyboardButton(
                            text="Oᴡɴᴇʀ",
                            url="https://t.me/Ishikki_Akabane"
                            ),
                        ],
                        
                    ],
                ),
            )
    else:
          update.effective_message.reply_video(
            ERI_VID, caption= "ᴍᴏsʜɪ ᴍᴏsʜɪ, Eʀɪ sᴘᴇᴀᴋɪɴɢ!!!\n<b>ʜᴀᴠᴇɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Hᴇʟᴘ ❔",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ 📢 ",
                            url="https://t.me/suppporttxd".format(SUPPORT_CHAT),
                        )
                    ],
                ]
            ),
        )


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update: Update, context: CallbackContext):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "⊷⊶⊷❍ ｢Help for {} module」❍⊶⊷⊶\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_video(
                random.choice(HELP_IMG),caption= f"ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏғ {module.capitalize()} ✨",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Hᴇʟᴘ ❔",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_video(
            random.choice(HELP_IMG), caption= "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴘᴏssɪʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs.✨",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Hᴇʟᴘ ❔",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


#------------------------------------------------------------------------------------
def vegeta_about_callback(update, context):        #Guide-0------
    query = update.callback_query
    if query.data == "vegeta_":
        query.message.edit_caption(
            "ʀᴀɴᴋ sʜᴏᴡs ʏᴏᴜʀ ʟᴇᴠᴇʟ. ɪᴛ ʙᴀsɪᴄᴀʟʟʏ ᴛᴇʟʟs ʜᴏᴡ ɢᴏᴏᴅ ʏᴏᴜ ᴀʀᴇ ɪɴ ᴛʜᴇ ɢᴀᴍᴇ."
            "\n❍ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ʀᴀɴᴋ ᴄᴏᴍᴍᴀɴᴅs ᴛʏᴘᴇ /help ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʀᴀɴᴋ ʙᴜᴛᴛᴏɴ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Rᴀɴᴋ", callback_data="vegeta_admin"),
                    InlineKeyboardButton(text="Tᴇʟᴇɢʀᴀᴘʜ", url="https://t.me/"),
                 ],
                 [
                    InlineKeyboardButton(text="Pᴏɪɴᴛs", callback_data="vegeta_notes"),
                    InlineKeyboardButton(text="Gᴜɪʟᴅ", callback_data="vegeta_support"),
                 ]
                ]
            ),
        )
    elif query.data == "vegeta_back":
        query.message.edit_caption(
            PM_START_TEXT.format(
                escape_markdown(first_name), escape_markdown(context.bot.first_name)
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Pʟᴀʏ",
                            url="t.me/Friendsdomain".format(
                                context.bot.username,
                            ),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Sᴜᴘᴘᴏʀᴛ",
                            url=f"https://t.me/{SUPPORT_CHAT}",
                        ),
                        InlineKeyboardButton(
                            text="Gᴜɪᴅᴇ",
                            callback_data="vegeta_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="kᴀᴢᴜᴍᴀ ᴄʟᴀɴ",
                            url="https://t.me/KazumaclanXD"
                        ),
                        InlineKeyboardButton(
                        text="Oᴡɴᴇʀ",
                        url="https://t.me/Ishikki_Akabane"
                        ),
                    ],
                        
                ],
            ),
        )
    elif query.data == "vegeta_admin":   #rank----------------
        query.message.edit_caption(
            "ʀᴀɴᴋ sʜᴏᴡs ʏᴏᴜʀ ʟᴇᴠᴇʟ. ɪᴛ ʙᴀsɪᴄᴀʟʟʏ ᴛᴇʟʟs ʜᴏᴡ ɢᴏᴏᴅ ʏᴏᴜ ᴀʀᴇ ɪɴ ᴛʜᴇ ɢᴀᴍᴇ."
            "\nᴀᴠᴀɪʟᴀʙʟᴇ ʀᴀɴᴋs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀʀᴇ :"
            "\nɢᴏᴅ       s-ᴄʟᴀss"
            "\nᴀ-ᴄʟᴀss   ʙ-ᴄʟᴀss"
            "\nᴄ-ᴄʟᴀss   ᴅ-ᴄʟᴀss"
            "\n**ɢᴏᴅs** ᴀʀᴇ ᴛʜᴇ ʜɪɢʜᴇsᴛ ʀᴀɴᴋ ᴡʜɪᴄʜ ᴄᴀɴ ʙᴇ ᴀᴄʜɪᴠᴇᴅ. ᴛʜᴇʏ ɢᴇᴛ sᴘᴄɪᴇʟ ᴀᴄᴄᴇss ᴏғ ᴛʜᴇ ʙᴏᴛ. **s-ᴄʟᴀss** ᴀʀᴇ ᴛʜᴏsᴇ ᴘᴇᴏᴘʟᴇ ᴡʜᴏ ɢᴇᴛs ᴄʜᴀɴᴄᴇ ᴛᴏ ʙᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ. **ᴀ-ᴄʟᴀss** ᴀʀᴇ ᴛʜᴏsᴇ ᴘᴇᴏᴘʟᴇ ᴡʜᴏ ᴄᴀɴ ʙᴇ ᴛʜᴇ ᴘᴀʀᴛ ᴏғ ᴛʜᴇ ᴍɪɴɪsᴛʀʏ. **ʙ-ᴄʟᴀss** ᴘᴇᴏᴘʟᴇ ᴄᴀɴ ᴀᴘᴘʟʏ ᴡᴏʀᴋ ɪɴ ᴛʜᴇ ᴍɪɴɪsᴛʀʏ, ɪғ ᴛʜᴇ ɢᴏᴅs ғᴇᴇʟs ʀɪɢʜᴛ, ᴛʜᴇɴ ᴀ ʙ-ᴄʟᴀss ᴜsᴇʀ ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴀ ᴘᴀʀᴛ ᴏғ ᴛʜᴇ ᴍɪɴɪsᴛʀʏ. **ᴄ-ᴄʟᴀss** ᴜsᴇʀ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴍᴜᴄʜ ᴘʀɪᴠᴀʟᴀɢᴇs, ᴛʜᴇʏ ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ɢᴜɪʟᴅs. **ᴅ-ᴄʟᴀss** ᴜsᴇʀ ᴀʀᴇ ᴀᴛ ᴛʜᴇ ʙᴏᴛᴛᴏᴍ ᴏғ ᴛʜɪs ʜᴇɪʀᴄʜʏ, ᴛʜᴇʏ sɪᴍᴘʟʏ ᴀʀᴇ ᴛʜᴇ ʙɪɢɪɴᴇʀs. ʙᴜᴛ ɪᴛ ᴅᴏɴ’ᴛ ᴛᴀᴋᴇ ᴍᴜᴄʜ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴠᴀɴᴄᴇ ᴛʜᴇɪʀ ʟᴇᴠᴇʟ ᴛᴏ ᴄ-ᴄʟᴀss. ᴀᴅᴠᴀɴᴄɪɴɢ ғʀᴏᴍ ᴄ-ᴄʟᴀss ᴛᴏ ʙ-ᴄʟᴀss ɪs ʙɪᴛ ᴛᴏᴜʜ. ᴛʜɪs ᴡᴀʏ ᴛʜᴇ ᴅɪғғɪᴄᴜʟᴛʏ ᴋᴇᴇᴘs ɪɴᴄʀᴇᴀsɪɴɢ ᴡʜᴇɴᴇᴠᴇʀ ʏᴏᴜ ᴀᴅᴀᴠᴀɴᴄᴇ ʏᴏᴜʀ ʀᴀɴᴋ."
            "\n❍ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ʀᴀɴᴋ ᴄᴏᴍᴍᴀɴᴅs ᴛʏᴘᴇ /help ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ɢᴀᴍᴇ ʙᴜᴛᴛᴏɴ.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="vegeta_")]]
            ),
        )

    elif query.data == "vegeta_notes":  #Points------------------
        query.message.edit_caption(
            "ᴘᴏɪɴᴛs ᴀʀᴇ ʟɪᴋᴇ ɢᴀᴍᴇ ᴄᴜʀʀᴇɴᴄʏ. ʏᴏᴜ ᴄᴀɴ ᴇᴀʀɴ ᴘᴏɪɴᴛs ɪɴ sᴇᴠᴇʀᴀʟ ᴡᴀʏs."
            "\nʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴘᴏɪɴᴛs ʙʏ ᴊᴏɪɴɪɴɢ ɢᴜɪʟᴅs, ʙʏ ᴄᴏᴍᴘʟᴇᴛɪɴɢ ᴊᴏʙ ʀᴇϙᴜᴇsᴛ."
            "\nᴛʜᴇʀᴇ ᴡɪʟʟ ʙᴇ ᴍᴀɴʏ ᴇᴠᴇɴᴛs ʜᴏsᴛᴇᴅ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ, ʏᴏᴜ ᴄᴀɴ ᴘᴀʀᴛɪᴄɪᴘᴀᴛᴇ ɪɴ ᴛʜᴀᴛ ᴇᴠᴇɴᴛ ᴀɴᴅ ᴄᴀɴ ɢᴇᴛ ᴘᴏɪɴᴛs, ʏᴏᴜ ᴄᴀɴ ᴇᴀʀɴ ᴇᴠᴇɴ ᴍᴏʀᴇ ʙʏ ᴀᴄʜɪᴇᴠɪɴɢ 1sᴛ, 2ɴᴅ  ᴀɴᴅ 3ʀᴅ ᴘʟᴀᴄᴇ ɪɴ ᴛʜᴇ ᴇᴠᴇɴᴛ. ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴇᴀʀɴ ᴘᴏɪɴᴛs ғᴏʀ ʏᴏᴜʀ ʀᴀɴᴋ, ᴛʜᴇ ᴍᴏʀᴇ ɪs ʏᴏᴜʀ ʀᴀɴᴋ ᴛʜᴇ ᴍᴏʀᴇ ᴘᴏɪɴᴛs ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴀs ᴀ ʀᴇᴡᴀʀᴅ ɪɴ ᴛʜᴇ ᴇɴᴅ ᴏғ ᴛʜᴇ ᴡᴇᴇᴋ."
            "\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴜsᴇ ᴘᴏʟɪᴛɪᴄᴀʟ ᴛʀɪᴄᴋs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴛᴏ ᴇᴀʀɴ ᴍᴏʀᴇ ᴘᴏɪɴᴛs ʙᴜᴛ ᴅᴏɴ’ᴛ ɢᴇᴛ ᴄᴀᴜɢʜᴛ."
            "\n❍ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘᴏɪɴᴛs ᴄᴏᴍᴍᴀɴᴅs ᴛʏᴘᴇ /help ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ɢᴀᴍᴇ ʙᴜᴛᴛᴏɴ.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="vegeta_")]]
            ),
        )
    elif query.data == "vegeta_support":   #Guild----------------
        query.message.edit_caption(
            "ʏᴏᴜ ᴄᴀɴ ᴇᴀʀɴ ᴇxᴛʀᴀ ᴘᴏɪɴᴛs ʙʏ ᴊᴏɪɴɪɴɢ ɢᴜɪʟᴅs. ᴀ ɢᴜɪʟᴅ ɢᴇᴛs ᴍᴏɴᴛʜʟʏ ʀᴇᴠᴇɴᴜᴇ ғʀᴏᴍ ᴛʜᴇ ᴍɪɴɪsᴛᴇʀs, ᴡʜɪᴄʜ ᴅɪʀᴇᴄᴛʟʏ ɢᴇᴛs sᴛᴏʀᴇᴅ ᴛᴏ ʏᴏᴜʀ ɢᴜɪʟᴅ sᴛᴏʀᴀɢᴇ ᴡʜɪᴄʜ ɪs ᴋᴇᴘᴛ sᴀғᴇ ʙʏ ᴛʜᴇ ɢᴏʙʟɪɴs. ᴀ ᴍᴇᴍʙᴇʀ ᴄᴀɴ ᴡɪᴛʜᴅʀᴀᴡ ᴛʜᴀᴛ ᴍᴏɴᴇʏ ғʀᴏᴍ ᴛʜᴇ sᴛᴏʀᴀɢᴇ ʙʏ ʀᴇϙᴜᴇsᴛɪɴɢ ᴛʜᴇ ɢᴏʙʟɪɴs. ʙᴇsɪᴅᴇs ᴛʜᴀᴛ, ᴀ sᴀʟᴀʀʏ ᴀᴍᴏᴜɴᴛ ɪs ᴀʟsᴏ ɢɪᴠᴇɴ ᴛᴏ ᴛʜᴇ ɢᴜɪʟᴅ ᴍᴇᴍʙᴇʀs. ᴛʜᴇ ᴀᴍᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʀᴇᴠᴇɴᴜᴇ ᴀɴᴅ sᴀʟᴀʀʏ ᴅᴇᴘᴇɴᴅs ᴏɴ ᴛʜᴇ ʟᴇᴠᴇʟ ᴏғ ᴛʜᴇ ɢᴜɪʟᴅ. ʏᴏᴜ ᴄᴀɴ ʟᴇᴠᴇʟ ᴜᴘ ʏᴏᴜʀ ɢᴜɪʟᴅ ʙʏ ʟᴇᴠᴇʟɪɴɢ ᴜᴘ ʏᴏᴜʀ ᴏᴡɴ ʀᴀɴᴋ ᴏʀ ᴄᴏᴍᴘʟᴇᴛɪɴɢ sᴏᴍᴇ ɢᴜɪʟᴅ ʀᴇϙᴜᴇsᴛ. ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ɢᴜɪʟᴅ."
            "\n❍ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ɢᴜɪʟᴅ ᴄᴏᴍᴍᴀɴᴅs ᴛʏᴘᴇ /help ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ɢᴀᴍᴇ ʙᴜᴛᴛᴏɴ. ",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="vegeta_")]]
            ),
        )


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 254318997 and DONATION_LINK:
            update.effective_message.reply_text(
                "You can also donate to the person currently running me "
                "[here]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    test_handler = CommandHandler("test", test, run_async=True)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)

    donate_handler = CommandHandler("donate", donate, run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    about_callback_handler = CallbackQueryHandler(
        vegeta_about_callback, pattern=r"vegeta_", run_async=True
    )

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
