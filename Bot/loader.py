from Bot.keys import API_ID, API_HASH, TOKEN, SESSION_NAME
from pyrogram import Client
from Defs.datastore import Rooms, Users, DataBot
from Defs.lang import Lang
from Data.config import workers, max_concurrent_transmissions
from Defs.logger import Logger


log = Logger(name="Main")

rooms = Rooms("Data/data.rooms.json")
users = Users("Data/data.users.json")
lang = Lang("Data/Langs", "ru")
databot = DataBot(logger=log)


bot = Client(
    name=SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN,

    workdir="Bot",

    workers=workers, max_concurrent_transmissions=max_concurrent_transmissions, 
)