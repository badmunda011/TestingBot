import Config
from pyrogram import Client

app = Client(
             name="TESTING", 
             api_id=Config.APP_ID, 
             api_hash=Config.HASH_ID, 
             bot_token=Config.TOKEN,
             plugins=dict(root="Testing")  # Ensure the plugins folder is structured correctly
)
)
