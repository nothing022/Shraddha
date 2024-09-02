import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from ShraddhaMusic import Carbon, YouTube, app
from ShraddhaMusic.core.call import Shraddha
from ShraddhaMusic.misc import db
from ShraddhaMusic.utils.database import add_active_video_chat, is_active_chat
from ShraddhaMusic.utils.exceptions import AssistantErr
from ShraddhaMusic.utils.inline import aq_markup, close_markup, stream_markup
from ShraddhaMusic.utils.pastebin import ShraddhaBin
from ShraddhaMusic.utils.stream.queue import put_queue, put_queue_index
from ShraddhaMusic.utils.thumbnails import gen_thumb


async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if forceplay:
        await Shraddha.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = f"{_['play_19']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    vidid,
                ) = await YouTube.details(search, False if spotify else True)
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:70]}\n"
                msg += f"{_['play_20']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                file_path, direct, error = await YouTube.download(vidid, mystic, video=status, videoid=True)
                if not file_path:
                    raise AssistantErr(f"""{_["play_14"]} \n\n Reason : {error}""")
                await Shraddha.join_call(
                    chat_id,
                    original_chat_id,
                    file_path,
                    video=status,
                    image=thumbnail,
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                img = await gen_thumb(vidid)
                button = stream_markup(_, chat_id)
                if config.PHOTO_THUMBNAIL:
                   run = await app.send_photo(original_chat_id,photo=img,caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name),reply_markup=InlineKeyboardMarkup(button))
                else:
                   run = await app.send_message(original_chat_id,text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name),reply_markup=InlineKeyboardMarkup(button),disable_web_page_preview=True)
                try:
                  db[chat_id][0]["mystic"] = run
                  db[chat_id][0]["markup"] = "stream"
                except IndexError:
                  await run.delete()
                  await app.send_message(original_chat_id,_["play_23"])
                await mystic.delete()
        if count == 0:
            return
        else:
            link = await ShraddhaBin(msg)
            lines = msg.count("\n")
            if lines >= 17:
                car = os.linesep.join(msg.split(os.linesep)[:17])
            else:
                car = msg
            carbon = await Carbon.generate(car, randint(100, 10000000))
            upl = close_markup(_)
            if config.PHOTO_THUMBNAIL:
               return await app.send_photo(original_chat_id,photo=carbon,caption=_["play_21"].format(position, link),reply_markup=upl)
            else:
               return await app.send_message(original_chat_id,text=_["play_21"].format(position, link),reply_markup=upl,disable_web_page_preview=True)
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        thumbnail = result["thumb"]
        status = True if video else None
        current_queue = db.get(chat_id)
        if current_queue is not None and len(current_queue) >= config.PLAYLIST_FETCH_LIMIT:
            return await app.send_message(original_chat_id, f"You can't add more than {str(config.PLAYLIST_FETCH_LIMIT)} songs to the queue.")
        file_path, direct, error = await YouTube.download(vidid, mystic, videoid=True, video=status)
        if not file_path:
           raise AssistantErr(f"""{_["play_14"]} \n\n Reason : {error}""")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(
                chat_id=original_chat_id,
                text=_["queue_4"].format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Shraddha.join_call(
                chat_id,
                original_chat_id,
                file_path,
                video=status,
                image=thumbnail,
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id)
            if config.PHOTO_THUMBNAIL:
              run = await app.send_photo(original_chat_id,photo=img,caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name,),reply_markup=InlineKeyboardMarkup(button))
            else:
              run = await app.send_message(original_chat_id,text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name,),reply_markup=InlineKeyboardMarkup(button),disable_web_page_preview=True)
            try:
              db[chat_id][0]["mystic"] = run
              db[chat_id][0]["markup"] = "stream"
            except IndexError:
              await run.delete()
              await app.send_message(original_chat_id,_["play_23"])
            await mystic.delete()
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(
                chat_id=original_chat_id,
                text=_["queue_4"].format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Shraddha.join_call(chat_id, original_chat_id, file_path, video=None)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=config.SOUNCLOUD_IMG_URL,
                caption=_["stream_1"].format(
                    config.SUPPORT_GROUP, title[:23], duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            try:
              db[chat_id][0]["mystic"] = run
              db[chat_id][0]["markup"] = "tg"
            except IndexError:
              await run.delete()
              await app.send_message(original_chat_id,_["play_23"])
            await mystic.delete()
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(
                chat_id=original_chat_id,
                text=_["queue_4"].format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Shraddha.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)
            button = stream_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=config.TELEGRAM_VIDEO_URL if video else config.TELEGRAM_AUDIO_URL,
                caption=_["stream_1"].format(link, title[:23], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            try:
              db[chat_id][0]["mystic"] = run
              db[chat_id][0]["markup"] = "tg"
            except IndexError:
              await run.delete()
              await app.send_message(original_chat_id,_["play_23"])
            await mystic.delete()
    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        thumbnail = result["thumb"]
        duration_min = "Live Track"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await app.send_message(
                chat_id=original_chat_id,
                text=_["queue_4"].format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr(_["str_3"])
            await Shraddha.join_call(
                chat_id,
                original_chat_id,
                file_path,
                video=status,
                image=thumbnail if thumbnail else None,
            )
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id)
            if config.PHOTO_THUMBNAIL:
              run = await app.send_photo(original_chat_id,photo=img,caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name),reply_markup=InlineKeyboardMarkup(button))
            else:
              run = await app.send_message(original_chat_id,text=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{vidid}",title[:23],duration_min,user_name),reply_markup=InlineKeyboardMarkup(button),disable_web_page_preview=True)
            try:
              db[chat_id][0]["mystic"] = run
              db[chat_id][0]["markup"] = "tg"
            except IndexError:
              await run.delete()
              await app.send_message(original_chat_id,_["play_23"])
            await mystic.delete()
    elif streamtype == "index":
        link = result
        title = "ɪɴᴅᴇx ᴏʀ ᴍ3ᴜ8 ʟɪɴᴋ"
        duration_min = "00:00"
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await mystic.edit_text(
                text=_["queue_4"].format(position, title[:27], duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Shraddha.join_call(
                chat_id,
                original_chat_id,
                link,
                video=True if video else None,
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=_["stream_2"].format(user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            try:
              db[chat_id][0]["mystic"] = run
              db[chat_id][0]["markup"] = "tg"
            except IndexError:
              await run.delete()
              await app.send_message(original_chat_id,_["play_23"])
            await mystic.delete()
