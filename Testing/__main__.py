import asyncio
import importlib
from Testing import app, Bad
from Testing.Modules import ALL_MODULES
import Config

from .logging import LOGGER

# MAIN FUNCTION
async def main():
    await app.start()
    await Bad.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Testing.Modules" + all_module)
    LOGGER("Testing.Modules").info("Successfully Imported Modules...")
    LOGGER("Testing").info("Bot Started Successfully...")
    await app.stop()
    await Bad.disconnect()
    LOGGER("Testing").info("Stopping Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
