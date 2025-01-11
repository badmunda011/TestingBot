from Testing import app, Bad
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
import psutil  # For system stats like CPU, RAM, etc.
from telethon import TelegramClient

# Function to get system stats
async def bot_sys_stats():
    # Using psutil to get system stats (example)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    up_time = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    
    return up_time, cpu, ram, disk

# Ping command
@app.on_message(filters.command(["ping", "alive"]))
async def ping_com(client, message: Message):
    start = datetime.now()
    
    # Perform ping using Pyrogram
    pytgping = await app.ping()
    
    # Perform ping using Telethon
    with TelegramClient('anon', api_id, api_hash) as telethon_client:
        telethon_ping = (await telethon_client(functions.PingRequest())).ping_ms

    # Get system stats (CPU, RAM, Disk)
    UP, CPU, RAM, DISK = await bot_sys_stats()

    # Calculate response time in milliseconds
    resp = (datetime.now() - start).microseconds / 1000

    # Send a simple reply with detailed stats
    await message.reply_text(
        f"🔔 **Ping Response**:\n\n"
        f"⏱ **Response Time**: {resp} ms\n"
        f"📡 **Bot Uptime**: {UP}\n"
        f"💻 **CPU Usage**: {CPU}%\n"
        f"🧠 **RAM Usage**: {RAM}%\n"
        f"💾 **Disk Usage**: {DISK}%\n"
        f"🌐 **Ping to TG Server (Pyrogram)**: {pytgping} ms\n"
        f"🌐 **Ping to TG Server (Telethon)**: {telethon_ping} ms\n\n"
        "Everything is running smoothly! 🚀"
    )
