from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_start_userrooms(data: types.CallbackQuery):
    if data.data == "start.userrooms":
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_start_userrooms(data))
async def open_profile_by_id(orig: Client, data: types.CallbackQuery):
    rdata = []
    text = "<b>Список ваших комнат</b>:"
    for i in users.get_user_rooms(data.from_user.id): 
        name = rooms.get_roomname_by_id(i)
        peer = rooms.get_number_users_in_room(i)
        peer_limit = rooms.get_peer_limit_by_room_id(i)
        text = text + f'\n{name}: ({peer}/{peer_limit if peer_limit else "∞"})'
        rdata.append([i, name])

        
    await data.message.edit_text(
        text=text,
        reply_markup=Keybords.get_list_rooms(room_ids=rdata)
    )
    

def is_open_room(data: types.CallbackQuery):
    if data.data.split("_")[0] == "openroom":
        return True
    
    return False

@bot.on_callback_query(lambda orig, data: is_open_room(data))
async def open_profile_by_id(orig: Client, data: types.CallbackQuery):
    room_id = data.data.split("_")[1]
    