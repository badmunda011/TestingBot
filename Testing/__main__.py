import logging
import asyncio
import importlib
from Testing import app, Bad, Sukh
from pyrogram import idle
from Testing.Modules import ALL_MODULES
from telethon import TelegramClient
import Config

# LOGGER HANDLER
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# MAIN FUNCTION
async def main():
    await app.start()
    await Bad.start()
    await Sukh.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Testing.Modules" + all_module)
    LOGGER("Testing.Modules").info("Successfully Imported Modules...")
    LOGGER("Testing").info("Bot Started Successfully...")
    await idle()
    await app.stop()
    await Bad.disconnect()
    await Sukh.stop()
    LOGGER("Testing").info("Stopping Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
