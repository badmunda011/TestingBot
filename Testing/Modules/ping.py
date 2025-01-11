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
    
    # Simulate a simple request to measure response time
    await client.get_me()
    resp = (datetime.now() - start).total_seconds() * 1000  # Convert to milliseconds

    # Get system stats (CPU, RAM, Disk)
    UP, CPU, RAM, DISK = await bot_sys_stats()

    # Send a simple reply with detailed stats
    await message.reply_text(
        f"🔔 **Ping Response**:\n\n"
        f"⏱ **Response Time**: {resp:.2f} ms\n"
        f"📡 **Bot Uptime**: {UP}\n"
        f"💻 **CPU Usage**: {CPU}%\n"
        f"🧠 **RAM Usage**: {RAM}%\n"
        f"💾 **Disk Usage**: {DISK}%\n"
        "Everything is running smoothly! 🚀"
    )
