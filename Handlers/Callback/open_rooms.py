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
        peer_limit = rooms.get_peer_limit_by_id(i)
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
    
    if int(data.from_user.id) == int(rooms.get_admins_by_id(room_id)): user_perm = "admin" 
    else: user_perm = "participant"


    await data.message.edit_text(
        text="""
<b>Вы открыли комнату</b>: {name}
<b>Ссылка на комнату</b>: <a href='https://t.me/Secret113Santabot?start={room_id}'>{room_id}</a>
<b>Лимит участников</b>: {limit}
<b>Правила комнаты</b>: {rules}
<b>Дата "Жеребьёвки"</b>: {date}
""".format(
    name=rooms.get_roomname_by_id(room_id),
    room_id=room_id,
    limit=rooms.get_peer_limit_by_id(room_id),
    rules=rooms.get_rules_by_id(room_id),
    date=rooms.get_date_roll_by_id(room_id),
    ),
    
    reply_markup=Keybords.get_panel_room(room_id=room_id, user_perm=user_perm, dir_cancel="start.userrooms")
    )   