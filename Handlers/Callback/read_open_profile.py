from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

# [lang._text(self._, "open_origin"), f"openprofile_{user_id}"],
# [lang._text(self._, "send_gift"), f"sendmessage_{user_id}"]

def is_read_open_profile(data: types.CallbackQuery):
    if data.data.split("_")[0] == "openprofile":
        return True
    return False


@bot.on_callback_query(lambda orig, data: is_read_open_profile(data))
async def read_open_profile(orig: Client, data: types.CallbackQuery):
    room_id = data.data.split("_")[1]
    user_id = data.data.split("_")[2]
    userdata = rooms.get_data_user_in_room_id(room_id=room_id, user_id=user_id)

    await data.message.edit_text(
        text=lang._text("read_open_profile.text.message").format(
            name=userdata["Name"],
            Age=userdata["Age"],
            Bio=userdata["Bio"],
            Wishlist=userdata["Wishlist"],
            Soc_Nets=userdata["Soc_Nets"],
            ),     
        reply_markup=Keybords.get_keys_open_room_profile(
            room_id=room_id, 
            user_id=user_id
            )
    )
