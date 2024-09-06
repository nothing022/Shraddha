from pyrogram import filters
from pyrogram.types import Message

from ShraddhaMusic import YouTube, app
from ShraddhaMusic.core.call import Shraddha
from ShraddhaMusic.misc import db
from ShraddhaMusic.utils import AdminRightsCheck, seconds_to_min
from ShraddhaMusic.utils.inline import close_markup
from config import BANNED_USERS
import asyncio


@app.on_message(
    filters.command(["seek", "cseek", "seekback", "cseekback"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def main_seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_20"])
    query = message.text.split(None, 1)[1].strip()
    seekcmd = message.command[0][-2]
    user = message.from_user
    inline = False
    if not query.isnumeric():
        return await message.reply_text(_["admin_21"])
    await seek_comm(cli,message,_ ,chat_id,query,seekcmd,user,inline)


async def seek_comm(cli,message,_ ,chat_id,query,seekcmd,user,inline):
    playing = db.get(chat_id)
    keyboard = None if inline else close_markup(_)
    if not playing:
        msg = await message.reply_text(_["queue_2"])
        try: await asyncio.sleep(6); return await msg.delete()
        except: return
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        msg = await message.reply_text(_["admin_22"])
        try: await asyncio.sleep(6); return await msg.delete()
        except: return
    file_path = playing[0]["file"]
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if seekcmd == "c":
        if (duration_played - duration_to_skip) <= 10:
            msg = await message.reply_text(text=_["admin_23"].format(seconds_to_min(duration_played),duration),reply_markup=keyboard)
            try: await asyncio.sleep(6); return await msg.delete()
            except: return
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            msg = await message.reply_text(text=_["admin_23"].format(seconds_to_min(duration_played), duration),reply_markup=keyboard)
            try: await asyncio.sleep(6); return await msg.delete()
            except: return
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_24"])
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            msg = await message.reply_text(_["admin_22"])
            try: await asyncio.sleep(6); return await msg.delete()
            except: return
    check = (playing[0]).get("speed_path")
    if check:
        file_path = check
    if "index_" in file_path:
        file_path = playing[0]["vidid"]
    try:
        await Shraddha.seek_stream(chat_id,file_path,seconds_to_min(to_seek),duration,playing[0]["streamtype"])
    except:
        msg = await mystic.edit_text(_["admin_26"], reply_markup=keyboard)
        try: await asyncio.sleep(6); return await msg.delete()
        except: return
    if seekcmd == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(text=_["admin_25"].format(seconds_to_min(to_seek),user.mention),reply_markup=keyboard)
    if inline:
       try: await asyncio.sleep(6); return await mystic.delete()
       except: return