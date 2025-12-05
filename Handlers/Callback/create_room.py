from Bot.loader import bot, lang, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_cancel_create_room(data: types.CallbackQuery):
    if data.data == "cancel.create_room": return True
    return False

def is_create_room(data: types.CallbackQuery):
    if data.data == "start.createroom": return True
    return False

def is_skip_create_room_peer_limit(data: types.CallbackQuery):
    if data.data == "skip.create_room.peer_limit": return True
    return False


@bot.on_callback_query(lambda orig, data: is_cancel_create_room(data))
async def cancel_create_room(origin: Client, data: types.CallbackQuery):
    await data.message.edit_text(text=lang._text("start_message"), reply_markup=Keybords.get_start())

@bot.on_callback_query(lambda orig, data: is_create_room(data))
async def create_room(origin: Client, data: types.CallbackQuery):
    users.set_add_user_status(data.from_user.id, "create_room")
    await data.message.edit_text(
        text=lang._text("newroom.name"), 
        reply_markup=Keybords.get_cancel("cancel.create_room")
        )
    
@bot.on_callback_query(lambda orig, data: is_skip_create_room_peer_limit(data))
async def skip_create_room_peer_limit(origin: Client, data: types.CallbackQuery):
    users.set_add_user_status(data.from_user.id, None)
    await data.message.edit_text(lang._text("newroom.peer_no_limit"))

    