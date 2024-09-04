import asyncio
import importlib

from pyrogram import idle
from pyrogram.errors import ChatAdminRequired

import config

from ShraddhaMusic import LOGGER, app, userbot
from ShraddhaMusic.core.call import Shraddha
from ShraddhaMusic.misc import sudo
from ShraddhaMusic.plugins import ALL_MODULES
from ShraddhaMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ShraddhaMusic.plugins" + all_module)
    LOGGER("ShraddhaMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Shraddha.start()
    try:
        await Shraddha.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except ChatAdminRequired:
        LOGGER("ShraddhaMusic").error(
            r"Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Shraddha.decorators()
    LOGGER("ShraddhaMusic").info("\x53\x68\x72\x61\x64\x64\x68\x61\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x53\x68\x72\x61\x64\x64\x68\x61\x43\x68\x61\x74")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("ShraddhaMusic").info("Stopping Shraddha Music Bot...")

if __name__ == "__main__":
    app.run(init())
