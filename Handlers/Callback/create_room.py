from Bot.loader import bot, lang
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

def is_create_room(data: types.CallbackQuery):
    if data.data == "start.createroom": return True
    return False

@bot.on_callback_query(lambda orig, data: is_create_room(data))
async def create_room(origin: Client, data: types.CallbackQuery):
    await data.message.edit_text(lang._text("newroom.name"))