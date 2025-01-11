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
    
    # Add a delay or wait for an event
    await asyncio.sleep(60)  # Sleep for 60 seconds

    await app.stop()
    await Bad.disconnect()
    LOGGER("Testing").info("Stopping Bot...")
