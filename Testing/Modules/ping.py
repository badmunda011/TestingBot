from Testing import app
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import psutil  # For system stats like CPU, RAM, etc.

# Replace these with appropriate imports or definitions
PING_IMG_URL = "https://te.legra.ph/file/b8a0c1a00db3e57522b53.jpg"  # URL for the ping image
BANNED_USERS = []  # List of banned users, could be set up as needed

# Function to get system stats
async def bot_sys_stats():
    # Using psutil to get system stats (example)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    up_time = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    
    return up_time, cpu, ram, disk

# Ping command
@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
async def ping_com(client, message: Message):
    start = datetime.now()

    # Send a reply with a ping image
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption="🏓 **Pong!**\n\nYour bot is alive and kicking! Let me check the status for you..."
    )

    # Perform ping using app (app.ping() is the method to ping Telegram servers)
    pytgping = await app.ping()

    # Get system stats (CPU, RAM, Disk)
    UP, CPU, RAM, DISK = await bot_sys_stats()

    # Calculate response time in milliseconds
    resp = (datetime.now() - start).microseconds / 1000

    # Prepare the inline keyboard buttons
    buttons = [
        [
            InlineKeyboardButton("Support", url="https://t.me/your_support_chat"),
            InlineKeyboardButton("Bot Info", callback_data="bot_info")
        ]
    ]

    # Edit the message with detailed stats and buttons
    await response.edit_text(
        f"🔔 **Ping Response**:\n\n"
        f"⏱ **Response Time**: {resp} ms\n"
        f"📡 **Bot Uptime**: {UP}\n"
        f"💻 **CPU Usage**: {CPU}%\n"
        f"🧠 **RAM Usage**: {RAM}%\n"
        f"💾 **Disk Usage**: {DISK}%\n"
        f"🌐 **Ping to TG Server**: {pytgping} ms\n\n"
        "Everything is running smoothly! 🚀",
        reply_markup=InlineKeyboardMarkup(buttons)  # Add inline buttons
    )
