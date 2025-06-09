import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x}
    
    DB_NAME = os.getenv("DB_NAME", "cocktail_bot_db")
    DB_USER = os.getenv("DB_USER", "bot_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

config = Config()