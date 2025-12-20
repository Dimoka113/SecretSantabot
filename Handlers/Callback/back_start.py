from Bot.loader import bot, lang, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_start_call(data: types.CallbackQuery):
    if data.data in ["start", "cancel.create_room"]:
        return True
    return False



@bot.on_callback_query(lambda orig, data: is_start_call(data))
async def start_call(orig: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    users.set_userdata_status_type(data.from_user.id, "")
    if users.is_users_exist(user_id):
        if len(users.get_user_rooms(user_id)) != 0:
            await data.message.edit_text(
                text=lang._text("start_message"), 
                reply_markup=Keybords.get_start_all(),
                disable_web_page_preview=config.disable_web_page_preview,
                )
        else:
            await data.message.edit_text(
                text=lang._text("start_message"), 
                reply_markup=Keybords.get_start_no_room(),
                disable_web_page_preview=config.disable_web_page_preview,
            )
    else:
        await data.message.edit_text(
            text=lang._text("start_message_noprofile"), 
            reply_markup=Keybords.create_profile(),
            disable_web_page_preview=config.disable_web_page_preview
            )
