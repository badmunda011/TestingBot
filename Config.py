from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
# Get this value from my.telegram.org/apps
API_HASH = getenv("API_HASH")
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")
