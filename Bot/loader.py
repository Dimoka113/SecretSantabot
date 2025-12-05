from Bot.keys import API_ID, API_HASH, TOKEN
from pyrogram import Client
from Defs.logger import Logger
from Defs.datastore import Rooms, Users
from Defs.lang import Lang
from Data.config import workers, max_concurrent_transmissions

Logger.level("INFO")
log = Logger(name="Main")

rooms = Rooms("Data/rooms.json")
users = Users("Data/users.json")
lang = Lang("Data/Langs", "ru")

bot = Client(
    name="SecretSanta", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN,

    workdir="Bot",

    workers=workers, max_concurrent_transmissions=max_concurrent_transmissions, 
)