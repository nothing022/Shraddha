#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/ShraddhaMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/ShraddhaMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import re 
import io
import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import filters,enums
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaAudio,
                            InputMediaVideo, Message)

from config import (BANNED_USERS, SONG_DOWNLOAD_DURATION,
                    SONG_DOWNLOAD_DURATION_LIMIT)
from ShraddhaMusic import YouTube,Instagram,app
from ShraddhaMusic.utils.decorators.language import language, languageCB
from ShraddhaMusic.utils.formatters import convert_bytes
from ShraddhaMusic.utils.inline.song import song_markup
import pyrogram 

@app.on_inline_query(~BANNED_USERS, group=0)
async def iginline(c,q):
  query = q.query
  if not (query and len(query.split(" ")) > 1 and query.split(" ")[0] == "!ig" and Instagram.exists(query.split(" ")[1])):
    return
  mediaid = query.split(" ")[1].split("/")
  res = pyrogram.types.InlineQueryResultPhoto(title="Download Instagram Video",photo_url="https://telegra.ph/file/2dbf6974c6bdc02be3f15.jpg",caption = f"Download Now : <a href={query.split(' ')[1]}>Insta Video</a>",reply_markup=pyrogram.types.InlineKeyboardMarkup([[pyrogram.types.InlineKeyboardButton(text="Download ⬇️", callback_data=f"igdownload:{mediaid[-2]}/{mediaid[-1]}")]]))
  if Instagram.is_valid_instagram_story_url(query.split(" ")[1]):
   mediaid = Instagram.filter_instagram_story_url(query.split(" ")[1]).split("/")
   res = pyrogram.types.InlineQueryResultPhoto(title="Download Instagram Video",photo_url="https://telegra.ph/file/2dbf6974c6bdc02be3f15.jpg",caption = f"Download Now : <a href={query.split(' ')[1]}>Insta Video</a>",reply_markup=pyrogram.types.InlineKeyboardMarkup([[pyrogram.types.InlineKeyboardButton(text="Download ⬇️", callback_data=f"igdownload:{mediaid[-3]}/{mediaid[-2]}/{mediaid[-1]}")]]))
  await q.answer([res],cache_time=10)


@app.on_callback_query(
    filters.regex(pattern=r"igdownload") & ~BANNED_USERS
)
@language
async def song_commad_private(client, query, _):
    url = f"https://www.instagram.com/{query.data.split(':')[-1]}"
    mystic = await app.edit_inline_text(inline_message_id=query.inline_message_id,text=_["play_1"]) 
    try:
      vidurl,picurl,name,typee = Instagram.info(url)
      instalink = f"https://www.instagram.com/{name}/"
      await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"<b>Downloading!</>\n\nInstagram media from  {name} \n\nUsage: <code>@mnrobot !ig url</code>")
      name,res = Instagram.instadl(url)
      await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"<b>Uploading!</>\n\nInstagram media from  {name} \n\nUsage: <code>@mnrobot !ig url</code>")
      if typee in [1,8]:
       with open(res, "rb") as photo_file:
         photo = io.BytesIO(photo_file.read())
       photo.name = "photo.jpg"
       await app.edit_inline_media(inline_message_id=query.inline_message_id,media= pyrogram.types.InputMediaPhoto(media=photo,caption=f"Instagram photo from <a href={instalink}> {name} </a>\n\nUsage: <code>@mnrobot !ig url</code>"))
      if typee == 2:
       await app.edit_inline_media(inline_message_id=query.inline_message_id,media= pyrogram.types.InputMediaVideo(media=res,caption=f"Instagram video from <a href={instalink}> {name} </a>\n\nUsage: <code>@mnrobot !ig url</code>"))
    except Exception as e:
      mystic = await app.edit_inline_text(inline_message_id=query.inline_message_id,text=f"Error: {e}")


@app.on_message(
    filters.command("insta")
    & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    if len(message.text.split(" ")) == 1:
     return await message.reply("Usage: /insta [Instagram URL]")
    url = message.text.split(" ")[1]
    if url:
        if not Instagram.exists(url):
            return await message.reply_text(_["song_5"].replace('Youtube ',''))
    mystic = await message.reply_text(_["play_1"])
    try:
      vidurl,picurl,name,typee = Instagram.info(url)
      instalink = f"https://www.instagram.com/{name}/"
      await mystic.edit(f"<b>Downloading!</>\n\nInstagram media from  {name} \n\nUsage: /insta [Instagram URL]")
      name,res = Instagram.instadl(url)
      await mystic.edit(f"<b>Uploading!</>\n\nInstagram media from  {name} \n\nUsage: /insta [Instagram URL]")
      await app.send_chat_action(
            chat_id=message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )
      if typee in [1,8]:
       await message.reply_document(res, caption=f"Instagram photo from <a href={instalink}> {name} </a>\n\nUsage: /insta [Instagram URL]")
      if typee == 2:
       await message.reply_video(res, caption=f"Instagram video from <a href={instalink}> {name} </a>\n\nUsage: /insta [Instagram URL]")
      await mystic.delete()
    except Exception as e:
      await message.reply(f"Error: {e}")
      await mystic.delete()


@app.on_message(
    filters.command("song")
    & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["song_12"].format(
                    SONG_DOWNLOAD_DURATION / 60, duration_min
                )
            )
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except Exception as e:
        return await mystic.edit_text(f"""{_["play_3"]}\n\nReason : {e}""")
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_back") & ~BANNED_USERS
)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_helper") & ~BANNED_USERS
)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(
                vidid, True
            )
        except:
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            check = x["format"]
            if "audio" in check:
                if x["filesize"] is None:
                    continue
                form = x["format_note"].title()
                if form not in done:
                    done.append(form)
                else:
                    continue
                sz = convert_bytes(x["filesize"])
                fom = x["format_id"]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Quality Audio = {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )
    else:
        try:
            formats_available, link = await YouTube.formats(
                vidid, True
            )
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        # AVC Formats Only [ YUKKI MUSIC BOT ]
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            check = x["format"]
            if x["filesize"] is None:
                continue
            if not (x["format_id"].isdigit() and int(x["format_id"]) in done):
                continue
            sz = convert_bytes(x["filesize"])
            ap = check.split("-")[1]
            to = f"{ap} = {sz}"
            keyboard.row(
                InlineKeyboardButton(
                    text=to,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )


# Downloading Songs Here


@app.on_callback_query(
    filters.regex(pattern=r"song_download") & ~BANNED_USERS
)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)
    thumb_image_path = await CallbackQuery.message.download()
    if stype == "video":
        thumb_image_path = await CallbackQuery.message.download()
        width = CallbackQuery.message.photo.width
        height = CallbackQuery.message.photo.height
        file_path, direct, error = await YouTube.download(yturl,mystic,songvideo=True,format_id=format_id,title=title)
        if not file_path:
            return await mystic.edit_text(_["song_9"].format(e) + f"\n\n Reason : {error}" )
        med = InputMediaVideo(
            media=file_path,
            duration=duration_sec,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)
    elif stype == "audio":
        try:
            filename, direct, error = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))
        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=vidid,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_AUDIO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(filename)
