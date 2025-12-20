from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

def is_give_datauser_room(data: types.CallbackQuery):
    if "giftuser_" in data.data:
        return True
    return False


@bot.on_callback_query(lambda orig, data: is_give_datauser_room(data))
async def give_datauser_room(origin: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id = data.data.split("_")
    rolled = rooms.get_roolled_by_id(room_id)

    if rolled:
        played = rolled[str(user_id)]
        try:
            played_data = await bot.get_chat(played)
            played_username_text = f"(@{played_data.username})" if played_data.username else ""
        except:
            played_username_text= ""

        await data.message.edit(
            text=lang._text("run_roll","text.message_private").format(
                name =rooms.get_data_user_in_room_id(room_id, played, "Name"),
                played = played, 
                played_username_text = played_username_text
            ),
            reply_markup=Keybords.get_keys_open_user_profile_back(room_id, played, f"openroom_{room_id}"),
            disable_web_page_preview=config.disable_web_page_preview
        )
    else:
        await data.answer(
            text=lang._text("roll.donot_runned.message"), 
            show_alert=True
        )