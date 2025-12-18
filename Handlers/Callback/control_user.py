from Bot.loader import bot, lang, users, rooms
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
                user=rooms.get_data_user_in_room_id(room_id, delete_user_id, "Name"), ),
            
            reply_markup=Keybords.get_keys_delete_user(room_id, delete_user_id, f"open.user_{room_id}_{delete_user_id}")
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
    else:
        await data.answer(
            text=lang._text("alerts", "notadmin"),
            show_alert=True
            )

