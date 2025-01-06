from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Get this value from my.telegram.org/apps
APP_ID = int(getenv("APP_ID"))
# Get this value from my.telegram.org/apps
HASH_ID = getenv("HASH_ID")
# Get your token from @BotFather on Telegram.
TOKEN = getenv("TOKEN")
