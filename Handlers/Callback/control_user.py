from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_delete_user_call(data: types.CallbackQuery):
    #  "delete.user_{room_id}_{user_id}"
    if "user.delete_" in data.data:
        return True
    return False

def is_delete_sure_user_call(data: types.CallbackQuery):
    #  "delete.user_{room_id}_{user_id}"
    if "user.suredelete_" in data.data:
        return True
    return False


@bot.on_callback_query(lambda orig, data: is_delete_user_call(data))
async def delete_user_call(orig: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id, delete_user_id = data.data.split("_")
    admin_id = rooms.get_admins_by_id(room_id)
    if user_id == admin_id:
        await data.message.edit_text(
            text=lang._text("delete.user.text").format(
                user=rooms.get_data_user_in_room_id(room_id, delete_user_id, "Name"), 
            ),
            reply_markup=Keybords.get_keys_delete_user(room_id, delete_user_id, f"open.user_{room_id}_{delete_user_id}"),
            disable_web_page_preview=config.disable_web_page_preview
        )
    else:
        await data.answer(
            text=lang._text("alerts", "notadmin"),
            show_alert=True
            )



@bot.on_callback_query(lambda orig, data: is_delete_sure_user_call(data))
async def sure_delete_user_call(orig: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id, delete_user_id = data.data.split("_")
    admin_id = rooms.get_admins_by_id(room_id)
    if user_id == admin_id:
        rooms.delete_user_in_room(room_id, delete_user_id)
        users.delete_user_in_room(room_id, delete_user_id)
        
        user_list = rooms.get_users_room_by_room_id(room_id)
        end = [[u_id, rooms.get_data_user_in_room_id(room_id, u_id)["Name"]] for u_id in user_list if u_id != admin_id]
        log.debug(end)
        await data.message.edit_text(
            text=lang._text("room.open_list_user") if len(end)>=1 else lang._text("room.open_list_user_only_admin"),
            reply_markup=Keybords.get_keys_list_users(
                room_id=room_id, 
                users=end, 
                dir_cancel=f"openroom_{room_id}"
            ),
            disable_web_page_preview=config.disable_web_page_preview
        )
        
    else:
        await data.answer(
            text=lang._text("alerts", "notadmin"),
            show_alert=True
            )

