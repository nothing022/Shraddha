import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from ShraddhaMusic import app
from ShraddhaMusic.misc import _boot_
from ShraddhaMusic.plugins.sudo.sudoers import sudoers_list
from ShraddhaMusic.utils.database import (
    add_served_chat,
    is_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShraddhaMusic.utils import bot_sys_stats
from ShraddhaMusic.utils.decorators.language import LanguageStart
from ShraddhaMusic.utils.formatters import get_readable_time
from ShraddhaMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from ShraddhaMusic.utils.inline.help import help_back_markup, private_help_panel

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
        if name[0:4] == ("help" if config.SEND_START_MESSAGE else "musi"):
          keyboard = help_pannel(_, True)
          UP, CPU, RAM, DISK = await bot_sys_stats()
          await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
            reply_markup=keyboard,)
          if await is_on_off(2):
            return await app.send_message(chat_id=config.LOG_GROUP_ID,text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}")
    elif config.SEND_START_MESSAGE:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )



@app.on_message(filters.command(["music"]) & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
  if message.chat.type != ChatType.PRIVATE:
   return await message.reply("ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴍᴜꜱɪᴄ ᴄᴏᴍᴍᴀɴᴅꜱ\n\n🎧 For change music playmode\n\n🤖 Click Here : /msettings",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text= "👤 ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ", url=f"https://t.me/{client.me.username.replace('@','')}?start=music")]]))
  keyboard = help_pannel(_, True)
  UP, CPU, RAM, DISK = await bot_sys_stats()
  await message.reply_photo(
    photo=config.START_IMG_URL,
    caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
    reply_markup=keyboard,)
  if await is_on_off(2):
    return await app.send_message(chat_id=config.LOG_GROUP_ID,text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",)

from pyrogram.enums import  ChatMemberStatus
new_mem = [ChatMemberStatus.BANNED,ChatMemberStatus.LEFT]


@app.on_message(group=8139)
async def update_old_chats(client,message):
  if message.chat.type != ChatType.SUPERGROUP:
    return
  if not await is_served_chat(message.chat.id):
    await add_served_chat(message.chat.id)

@app.on_chat_member_updated()
async def update_chats(client,update):
 if (not update.old_chat_member) or (update.old_chat_member and update.old_chat_member.status in new_mem):
        try:
            language = await get_lang(update.chat.id)
            _ = get_string(language)
            if not update.new_chat_member.user:
              return
            if await is_banned_user(update.new_chat_member.user.id):
                try:
                    await update.chat.ban_member(update.new_chat_member.user.id)
                except:
                    pass
            if update.new_chat_member.user.id == app.id:
                if update.chat.type != ChatType.SUPERGROUP:
                    await client.send_message(update.chat.id,_["start_4"])
                    return await app.leave_chat(update.chat.id)
                if update.chat.id in await blacklisted_chats():
                    await client.send_message(update.chat.id,
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(update.chat.id)

                out = start_panel(_)
                await client.send_photo(update.chat.id,
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        update.from_user.first_name,
                        app.mention,
                        update.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(update.chat.id)
        except Exception as ex:
            print(ex)