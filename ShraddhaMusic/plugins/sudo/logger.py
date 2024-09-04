from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram import __version__ as pyrover
from pytgcalls.__version__ import __version__ as pytgver

from ShraddhaMusic import app
from ShraddhaMusic.misc import SUDOERS
from ShraddhaMusic.utils.database import add_off, add_on, is_on_off
from ShraddhaMusic.utils.decorators.language import language
from ShraddhaMusic.utils import bot_sys_stats
from ShraddhaMusic.plugins import ALL_MODULES
from ShraddhaMusic.utils.inline import close_markup

import platform
from sys import version as pyver
import psutil
from datetime import datetime, timedelta

@app.on_message(filters.command(["logger"]) & SUDOERS)
@language
async def logger(client, message, _):
    zerostate = await is_on_off(2)
    usage = f"""{_["log_1"]}\n\nCurrent Status : {zerostate}"""
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state in ["enable","on","yes"]:
        await add_on(2)
        await message.reply_text(_["log_2"])
    elif state in ["disable","off","no"]:
        await add_off(2)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)

@app.on_message(filters.command(["cookies"]) & SUDOERS)
@language
async def logger(client, message, _):
    await message.reply_document("cookies/logs.csv")
    await message.reply_text("Please check given file to cookies file choosing logs...")


@app.on_message(filters.command(["sysinfo","systeminfo"]) & SUDOERS)
@language
async def sysinfocmd(client,message,_):
   inline = False
   await sysinfo(client,message,_,inline)

@app.on_callback_query(filters.regex("refreshsysinfo") & ~ SUDOERS)
@language
async def sysinfocmd(client, update,_):
   await update.answer("❌ ONLY SUDO USERS ALLOWED TO REFRESH STATS❗", show_alert=True)

@app.on_callback_query(filters.regex("refreshsysinfo") & SUDOERS)
@language
async def sysinfocmd(client, update,_):
   inline = True
   message = update.message
   await sysinfo(client,message,_,inline)
   await update.answer("🖥️ System stats updated❗")


async def sysinfo(client,message,_,inline):
    UP, CPU, RAM, DISK = await bot_sys_stats()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    uptime_str = str(timedelta(seconds=int(uptime.total_seconds())))
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram_total = psutil.virtual_memory().total / (1024.0**3)
    ram_used = psutil.virtual_memory().used / (1024.0**3)
    ram_free = psutil.virtual_memory().available / (1024.0**3)
    ram_total_str = f"{round(ram_total, 2)} ɢʙ"
    ram_used_str = f"{round(ram_used, 2)} ɢʙ"
    ram_free_str = f"{round(ram_free, 2)} ɢʙ"
    cpu_load = psutil.getloadavg()  # Load average for 1, 5, and 15 minutes
    cpu_load_formatted = ', '.join(f"{load:.2f}" for load in cpu_load)
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except Exception:
        cpu_freq = "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    free = hdd.free / (1024.0**3)
    text = ("➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        f"<b>Bot Uptime :</b> <code>{UP}</code>\n"
        f"<b>System Uptime :</b> <code>{uptime_str}</code>\n"
        f"<b>Server Storage:</b> <code>{DISK}</code>\n"
        f"<b>Cpu Usage :</b> <code>{CPU}</code>\n"
        f"<b>CPU Frequency :</b> <code>{cpu_freq}</code>\n"
        f"<b>CPU Load :</b> <code>{cpu_load_formatted}</code>\n"
        f"<b>Physical Cores :</b> <code>{p_core}</code>\n"
        f"<b>Logical Cores :</b> <code>{t_core}</code>\n"
        f"<b>RAM Consumption :</b> <code>{RAM}</code>\n"
        f"<b>Total RAM :</b> <code>{ram_total_str}</code>\n"
        f"<b>Used RAM :</b> <code>{ram_used_str}</code>\n"
        f"<b>Free RAM :</b> <code>{ram_free_str}</code>\n"
        f"<b>Storage Available :</b> <code>{str(total)[:4]} GB</code>\n"
        f"<b>Storage Used :</b> <code>{str(used)[:4]} GB</code>\n"
        f"<b>Storage Free :</b> <code>{str(free)[:4]} GB</code>\n"
        f"<b>Modules :</b> <code>{len(ALL_MODULES)}</code>\n"
        f"<b>Platforms :</b> <code>{platform.system()}</code>\n"
        f"<b>Python :</b> <code>{pyver.split()[0]}</code>\n"
        f"<b>Pyrogram :</b> <code>{pyrover}</code>\n"
        f"<b>Py-TgCalls :</b> <code>{pytgver}</code>\n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⍟ ʀᴇꜰʀᴇꜱʜ ⍟",callback_data="refreshsysinfo")],[InlineKeyboardButton("⍟ ᴄʟᴏꜱᴇ ⍟",callback_data="close")]])
    if inline:
       await message.edit_text(text,reply_markup = keyboard)
    else:        
       await message.reply_text(text,reply_markup = keyboard)
