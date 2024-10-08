from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from ShraddhaMusic import app
from ShraddhaMusic.core.call import Shraddha
from ShraddhaMusic.utils import bot_sys_stats
from ShraddhaMusic.utils.decorators.language import language
from ShraddhaMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL
import config

@app.on_message(filters.command(["ping","mping","malive","alive"] if config.SEND_START_MESSAGE else ["mping", "malive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Shraddha.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
