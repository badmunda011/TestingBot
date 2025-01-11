import os
import asyncio
import logging
from Testing import app, Bad
from pyrogram import filters
from pyrogram.types import Message

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
    
# Load installed plugins from file
def load_installed_plugins():
    if os.path.exists("installed_plugins.txt"):
        with open("installed_plugins.txt", "r") as file:
            return set(file.read().splitlines())
    return set()

# Save installed plugins to file
def save_installed_plugins(plugins):
    with open("installed_plugins.txt", "w") as file:
        file.write("\n".join(plugins))

installed_plugins = load_installed_plugins()

# Load installed plugins at startup
for plugin in installed_plugins:
    try:
        __import__(plugin)
        logger.info(f"Loaded plugin: {plugin}")
    except ImportError as e:
        logger.error(f"Failed to load plugin {plugin}: {str(e)}")

# Function to check if a plugin is already installed
def is_plugin_installed(plugin_name):
    return plugin_name in installed_plugins

# Modified install command
@app.on_message(filters.command("install") & ~filters.forwarded & ~filters.via_bot)
async def install_plugin(client, message):
    if message.reply_to_message and message.reply_to_message.document:
        # Handle installation from a .py file reply
        try:
            document = message.reply_to_message.document
            plugin_name = os.path.splitext(document.file_name)[0]
            if is_plugin_installed(plugin_name):
                return await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' is already installed.</b>")

            file_path = await client.download_media(document)
            with open(file_path, "r") as file:
                code = file.read()
            
            # Save the code to new .py files for both Pyrogram and Telethon
            with open(f"pyrogram_{plugin_name}.py", "w") as plugin_file_pyrogram, open(f"telethon_{plugin_name}.py", "w") as plugin_file_telethon:
                plugin_file_pyrogram.write(code)
                plugin_file_telethon.write(code)
            
            # Verify the plugin import
            try:
                __import__(f"pyrogram_{plugin_name}")
                __import__(f"telethon_{plugin_name}")
                installed_plugins.add(plugin_name)
                save_installed_plugins(installed_plugins)
                await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' installed successfully for both Pyrogram and Telethon from file.</b>")
                logger.info(f"Plugin '{plugin_name}' installed successfully for both Pyrogram and Telethon from file.")
            except ImportError as e:
                await edit_or_reply(message, text=f"<b>Failed to import plugin '{plugin_name}':</b>\n<pre>{str(e)}</pre>")
                logger.error(f"Failed to import plugin '{plugin_name}': {str(e)}")
        except Exception as e:
            await edit_or_reply(message, text=f"<b>Failed to install plugin from file:</b>\n<pre>{str(e)}</pre>")
            logger.error(f"Failed to install plugin from file: {str(e)}")
    else:
        # Handle installation from command text
        if len(message.command) < 2:
            return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/install <plugin_code>")
        try:
            plugin_code = message.text.split(" ", maxsplit=1)[1].strip()
            plugin_name = "custom_plugin"
            if is_plugin_installed(plugin_name):
                return await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' is already installed.</b>")

            with open(f"pyrogram_{plugin_name}.py", "w") as plugin_file_pyrogram, open(f"telethon_{plugin_name}.py", "w") as plugin_file_telethon:
                plugin_file_pyrogram.write(plugin_code)
                plugin_file_telethon.write(plugin_code)
            
            # Verify the plugin import
            try:
                __import__(f"pyrogram_{plugin_name}")
                __import__(f"telethon_{plugin_name}")
                installed_plugins.add(plugin_name)
                save_installed_plugins(installed_plugins)
                await edit_or_reply(message, text=f"<b>Plugin installed successfully for both Pyrogram and Telethon from command.</b>")
                logger.info("Plugin installed successfully for both Pyrogram and Telethon from command.")
            except ImportError as e:
                await edit_or_reply(message, text=f"<b>Failed to import plugin:</b>\n<pre>{str(e)}</pre>")
                logger.error(f"Failed to import plugin: {str(e)}")
        except Exception as e:
            await edit_or_reply(message, text=f"<b>Failed to install plugin from command:</b>\n<pre>{str(e)}</pre>")
            logger.error(f"Failed to install plugin from command: {str(e)}")

# Modified uninstall command
@app.on_message(filters.command("uninstall") & ~filters.forwarded & ~filters.via_bot)
async def uninstall_plugin(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/uninstall <plugin_name>")
    plugin_name = message.text.split(" ", maxsplit=1)[1].strip()
    try:
        os.remove(f"pyrogram_{plugin_name}.py")
        os.remove(f"telethon_{plugin_name}.py")
        await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' uninstalled successfully for both Pyrogram and Telethon.</b>")
        logger.info(f"Plugin '{plugin_name}' uninstalled successfully for both Pyrogram and Telethon.")
    except Exception as e:
        await edit_or_reply(message, text=f"<b>Failed to uninstall plugin '{plugin_name}':</b>\n<pre>{str(e)}</pre>")
        logger.error(f"Failed to uninstall plugin '{plugin_name}': {str(e)}")

# Restart command to ensure commands persist across restarts
@app.on_message(filters.command("rs") & ~filters.forwarded & ~filters.via_bot)
async def restart(client, message):
    reply = await message.reply_text("**🔁 Restarting...**")
    await message.delete()
    await reply.edit_text("Successfully Restarted\nPlease wait 1-2 min for loading user plugins...")
    logger.info("Bot is restarting...")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")
