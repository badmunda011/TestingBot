import os
import sys
import asyncio
import importlib
from Testing import app, Bad
from pyrogram import filters
from Testing.logging import LOGGER
from pyrogram.types import Message

# Restart command to ensure commands persist across restarts
@app.on_message(filters.command("rs") & ~filters.forwarded & ~filters.via_bot)
async def restart(client, message):
    reply = await message.reply_text("**🔁 Restarting...**")
    await message.delete()
    await reply.edit_text("Successfully Restarted\nPlease wait 1-2 min for loading user plugins...")
    logger.info("Bot is restarting...")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")
