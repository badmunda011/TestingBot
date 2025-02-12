from pyrogram import Client
from telethon import TelegramClient
from telegram.ext import Application
import Config

# Pyrogram Client
app = Client(
    name="app",
    api_id=Config.APP_ID,
    api_hash=Config.HASH_ID,
    bot_token=Config.TOKEN,
    plugins=dict(root="Bad.Modules")
)

# Telethon Client
Bad = TelegramClient(
    session="Bad",
    api_id=Config.APP_ID,
    api_hash=Config.HASH_ID
).start(bot_token=Config.TOKEN)

from telegram.ext import Application
import Config

# Initialize Telegram Bot
Sukh = Application.builder().token(Config.TOKEN).build()

async def initialize_bot():
    await Sukh.initialize()  # ✅ Properly awaiting the coroutine

# Initialize the bot properly
asyncio.run(initialize_bot())  # ✅ Ensure initialization before starting
