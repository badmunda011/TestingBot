import os
import sys
import asyncio
import importlib
from Testing import app, Bad
from pyrogram import filters
from inspect import getfullargspec
from Testing.logging import LOGGER
from pyrogram.types import Message

logger = LOGGER(__name__)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})

import importlib
import os
import sys
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message

# Create a folder for plugins if it doesn't exist
os.makedirs("Testing/Modules", exist_ok=True)


@app.on_message(filters.command("install") & ~filters.forwarded & ~filters.via_bot)
async def install_plugins(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("Reply to a plugin file to install it.", quote=True)

    msg = await message.reply_text("**Installing...**", quote=True)
    plugin_path = await message.reply_to_message.download("Testing/Modules/")

    if not plugin_path.endswith(".py"):
        os.remove(plugin_path)
        return await msg.edit("**Invalid Plugin:** Not a Python file.")

    plugin_name = Path(plugin_path).stem
    try:
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        load = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(load)
        sys.modules[f"plugins.{plugin_name}"] = load
        await msg.edit(f"**Installed Successfully:** `{plugin_name}.py`")
    except Exception as e:
        await msg.edit(f"**Error:** {str(e)}")
        os.remove(plugin_path)


@app.on_message(filters.command("uninstall") & ~filters.forwarded & ~filters.via_bot)
async def uninstall_plugins(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Provide the plugin name to uninstall.", quote=True)

    plugin_name = message.command[1].strip().replace(".py", "")
    plugin_path = f"Testing/Modules/{plugin_name}.py"

    if not os.path.exists(plugin_path):
        return await message.reply_text(f"**Plugin Not Found:** `{plugin_name}`", quote=True)

    try:
        os.remove(plugin_path)
        sys.modules.pop(f"plugins.{plugin_name}", None)
        await message.reply_text(f"**Uninstalled Successfully:** `{plugin_name}.py`", quote=True)
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}", quote=True)

# Restart command to ensure commands persist across restarts
@app.on_message(filters.command("rs") & ~filters.forwarded & ~filters.via_bot)
async def restart(client, message):
    reply = await message.reply_text("**🔁 Restarting...**")
    await message.delete()
    await reply.edit_text("Successfully Restarted\nPlease wait 1-2 min for loading user plugins...")
    logger.info("Bot is restarting...")
    os.execv(sys.executable, ['python3'] + sys.argv)
