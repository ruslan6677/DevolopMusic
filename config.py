import os

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID", 6))
    API_HASH = os.environ.get("API_HASH", None)
    BOT_OWNER = os.environ.get("BOT_OWNER", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "MusicAzBot")
    PLAYLIST_NAME = os.environ.get("PLAYLIST_NAME", None)
    PLAYLIST_ID = int(os.environ.get("PLAYLIST_ID", None))
