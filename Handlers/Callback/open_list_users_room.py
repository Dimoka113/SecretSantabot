from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

def is_open_list_users_room(data: types.CallbackQuery):
    if "listusers_" in data.data:
        return True

@bot.on_callback_query(lambda orig, data: is_open_list_users_room(data))
async def open_list_users_room(origin: Client, data: types.CallbackQuery):
    _, room_id = data.data.split("_")
    admin_id = int(rooms.get_admins_by_id(room_id))
    user_list = rooms.get_users_room_by_room_id(room_id)
    end = [[u_id, rooms.get_data_user_in_room_id(room_id, u_id)["Name"]] for u_id in user_list if u_id != admin_id]
    log.debug(end)

    await data.message.edit_text(
        text=lang._text("room.open_list_user") if len(end)>=1 else lang._text("room.open_list_user_only_admin"),
        reply_markup=Keybords.get_keys_list_users(
            room_id=room_id, users=end, dir_cancel=f"openroom_{room_id}"
        ),
        disable_web_page_preview=config.disable_web_page_preview
    )


# f"open.user_{room_id}_{i[0]}"

def is_open_user_in_listusers(data: types.CallbackQuery):
    if "open.user_" in data.data:
        return True
    
@bot.on_callback_query(lambda orig, data: is_open_user_in_listusers(data))
async def open_user_in_room(origin: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id, open_user_id = data.data.split("_")
    admin_id = int(rooms.get_admins_by_id(room_id))
    user_data = rooms.get_data_user_in_room_id(room_id, open_user_id)

    if user_id == admin_id:
        reply_markup = Keybords.get_keys_control_user(room_id, open_user_id, f"listusers_{room_id}")
    # elif ...

    else:
        reply_markup = Keybords.get_cancel(f"listusers_{room_id}")
    
    await data.message.edit_text(
        text=lang._text("open_list_users_room", "text.open.profile.in_room").format(
            name=user_data["Name"],
            age=user_data["Age"],
            bio=user_data["Bio"],
            wishlist=user_data["Wishlist"],
            links=user_data["Soc_Nets"],
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=config.disable_web_page_preview
    )