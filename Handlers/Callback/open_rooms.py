from Bot.loader import bot, lang, users, rooms, databot
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
    text = ""
    emoji_partic = lang._text("emoji_participant")
    emoji_admin = lang._text("emoji_admin")
    
    for i in users.get_user_rooms(data.from_user.id): 
        admin_id = rooms.get_admins_by_id(i)
        name = rooms.get_roomname_by_id(i)
        peer = rooms.get_number_users_in_room(i)
        peer_limit = rooms.get_peer_limit_by_id(i)
        text = text + f'\n{name}: ({peer}/{peer_limit if peer_limit else "∞"})'
        
        if data.from_user.id == admin_id:
            rdata.append([i, name + " " + emoji_admin])
        #elif .. coadmin
        else:
            rdata.append([i, name + " " + emoji_partic])


    await data.message.edit_text(
        text=text,
        reply_markup=Keybords.get_list_rooms(room_ids=rdata),
        disable_web_page_preview=config.disable_web_page_preview,
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
        text = lang._text("open_rooms","text.message.edit_text")
        .format(
            botusername=databot.username,
            name=rooms.get_roomname_by_id(room_id),
            room_id=room_id,
            limit=rooms.get_peer_limit_by_id(room_id),
            rules=rooms.get_rules_by_id(room_id),
            date=rooms.get_date_roll_by_id(room_id),
        ),
        reply_markup=Keybords.get_panel_room(room_id=room_id, user_perm=user_perm, dir_cancel="start.userrooms"),
        disable_web_page_preview=config.disable_web_page_preview,
    )   


def is_openroomprofile(data: types.CallbackQuery):
    if "back.openroomprofile" in data.data:
        return 1
    elif "openroomprofile" in data.data:
        return 2
    else:
        return 0
    

@bot.on_callback_query(lambda orig, data: is_openroomprofile(data))
async def openroomprofile(orig: Client, data: types.CallbackQuery):
    call_data = is_openroomprofile(data)
    user_id = data.from_user.id
    room_id = data.data.split("_")[1]
    
    if call_data == 1:
        reply_markup = Keybords.get_keys_open_user_profile_back(room_id, user_id, f"openroom_{room_id}")
    else:
        reply_markup = Keybords.get_keys_open_user_profile(room_id, user_id)

    await data.message.edit_text(
        text = lang._text("open_rooms","text.message.edit_text")
        .format(
            botusername=databot.username,
            name=rooms.get_roomname_by_id(room_id),
            room_id=room_id,
            limit=rooms.get_peer_limit_by_id(room_id),
            rules=rooms.get_rules_by_id(room_id),
            date=rooms.get_date_roll_by_id(room_id),
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=config.disable_web_page_preview
    )