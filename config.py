import os

class Config:
    BOT_TOKEN = os.environ.get("5802781802:AAHTqszeFIeFw3DZgGAQn34HVdrELadC0TI")
    API_ID = int(os.environ.get("10300036"))
    API_HASH = os.environ.get("79c295e05c970ddd724f0762ba275104")
    BOT_OWNER = os.environ.get("ordayam_5_deqiqeye")
    BOT_USERNAME = os.environ.get("DevolopMusic_bot")
    PLAYLIST_NAME = os.environ.get("DevolopMusicingPlaylist")
    CHANNEL = os.environ.get("TheBorzMar")
    PLAYLIST_ID = int(os.environ.get("PLAYLIST_ID", "-1001664626884"))
    ETIRAF_BOT = os.environ.get("DevolopEtiraflar")
    ETIRAF_KANALI = os.environ.get("DevolopEtiraflar")
