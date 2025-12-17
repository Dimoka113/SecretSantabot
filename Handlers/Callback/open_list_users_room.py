from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

def is_open_list_users_room(data: types.CallbackQuery):
    if "listusers_" in data.data:
        return True

@bot.on_callback_query(lambda orig, data: is_open_list_users_room(data))
async def open_list_users_room(origin: Client, data: types.CallbackQuery):

    
    await data.message.edit_text(
        text=lang._text("room.open_list_user"),
        reply_markup=
    )
