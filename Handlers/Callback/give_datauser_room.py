from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

def is_give_datauser_room(data: types.CallbackQuery):
    if "userdata_" in data.data:
        return True
    return False


@bot.on_callback_query(lambda orig, data: is_give_datauser_room(data))
async def give_datauser_room(origin: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id = data.data.split("_")
    
    userdata = rooms.get_data_user_in_room_id(room_id, user_id)

    await data.edit_message_text(
        text = lang._text("formating_profile_status","profile")
            .format(
                name=userdata["Name"] if userdata["Name"] else lang._text("data.null"), 
                age=userdata["Age"] if userdata["Age"] else lang._text("data.null"), 
                bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"), 
                wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),  
                links=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"), 
        ),
        reply_markup=Keybords.keys_open_profile_in_room(room_id, f"openroom_{room_id}"),
        disable_web_page_preview=config.disable_web_page_preview
    )


def is_edit_profile_in_room(data: types.CallbackQuery):
    if "dataroom.edit" in data.data:
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_edit_profile_in_room(data))
async def edit_profile(origin: Client, data: types.CallbackQuery):
    edit = data.data.split(".")[1]
    calldata = data.data.split(".")[2]
    room_id = edit.split("_")[1]

    back_keys = Keybords.get_cancel(f"userdata_{room_id}")

    if calldata == "change_name": text = lang._text("formating_profile_status","edit_predone_profile","text.change_name")
    elif calldata == "change_age": text = lang._text("formating_profile_status","edit_predone_profile","text.change_age")
    elif calldata == "change_bio": text = lang._text("formating_profile_status","edit_predone_profile","text.change_bio")
    elif calldata == "change_wishlist": text = lang._text("formating_profile_status","edit_predone_profile","text.change_wishlist")
    elif calldata == "change_netlinks": text = lang._text("formating_profile_status","edit_predone_profile","text.change_netlinks")
    else: log.warn(f"Not suppoted calldata: {calldata} (give_datauser_room)"); return False

    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.set_userdata_status_type(data.from_user.id, f"dataroom.edit_{room_id}.{calldata}")
    await data.edit_message_text(
        text=text, 
        reply_markup=back_keys,
        disable_web_page_preview=config.disable_web_page_preview
    )