import os
import shutil
import asyncio

import subprocess
import sys
import traceback
import logging
from inspect import getfullargspec
from io import StringIO
from time import time
from pyrogram.types import BotCommand
from pyrogram import filters, Client as PyroClient, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telethon import TelegramClient, events, Button
from telethon.tl.custom import Button

@app.on_message(filters.command("rs") & ~filters.forwarded & ~filters.via_bot)
async def restart(client: PyroClient, message: Message):
    reply = await message.reply_text("**🔁 Restarting...**")
    await message.delete()
    await reply.edit_text("Successfully Restarted\nPlease wait 1-2 min for loading user plugins...")
    logger.info("Bot is restarting...")
    os.system(f"kill -9 {os.getpid()} && python3 -m Testing")
        
