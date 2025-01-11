import Config
from pyrogram import Client
from telethon import TelegramClient

# Pyrogram Client
app = Client(
             name="app", 
             api_id=Config.APP_ID, 
             api_hash=Config.HASH_ID, 
             bot_token=Config.TOKEN,
             plugins=dict(root="Testing.Modules")
)

# Telethon Bot
Bad = TelegramClient(
             session="Bad",  # Add a session name here
             api_id=Config.APP_ID, 
             api_hash=Config.HASH_ID
             ).start(bot_token=Config.TOKEN)

plugins = dict(root="Testing.Modules")
