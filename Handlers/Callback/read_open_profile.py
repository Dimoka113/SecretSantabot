from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

# [lang._text(self._, "open_origin"), f"openprofile_{user_id}"],
# [lang._text(self._, "send_gift"), f"sendmessage_{user_id}"]

def is_read_open_profile(data: types.CallbackQuery):
    if "back.openprofile_" in data.data:
        return 1
    elif "openprofile_" in data.data:
        return 2
    else:
        return 0


@bot.on_callback_query(lambda orig, data: is_read_open_profile(data))
async def read_open_profile(orig: Client, data: types.CallbackQuery):
    typecall = is_read_open_profile(data)

    room_id = data.data.split("_")[1]
    user_id = data.data.split("_")[2]
    userdata = rooms.get_data_user_in_room_id(room_id=room_id, user_id=user_id)

    if typecall == 2:
        reply_markup = Keybords.get_keys_open_room_profile(room_id=room_id, user_id=user_id)
    else:
        reply_markup = Keybords.get_keys_open_room_profile_back(room_id=room_id, user_id=user_id, dir_cancel=f"openroom_{room_id}")

    await data.message.edit_text(
        text=lang._text("read_open_profile.text.message").format(
            name=userdata["Name"] if userdata["Name"] else lang._text("data.null"),
            Age=userdata["Age"] if userdata["Age"] else lang._text("data.null"),
            Bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"),
            Wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),
            Soc_Nets=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"),
            ),     
        reply_markup=reply_markup,
        disable_web_page_preview=config.disable_web_page_preview
    )
