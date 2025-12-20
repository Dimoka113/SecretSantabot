from Bot.loader import bot, lang, users, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_open_profile(data: types.CallbackQuery):
    if data.data == "start.userprofile": return True
    return False

def is_edit_profile(data: types.CallbackQuery):
    if data.data == "start.main": return True
    return False


@bot.on_callback_query(lambda orig, data: is_open_profile(data))
async def open_profile_message(origin: Client, data: types.CallbackQuery):
    userdata = users.get_user_by_id(data.from_user.id)
    await data.edit_message_text(
        text=lang._text("formating_profile_status","profile").format(
            name=userdata["Name"] if userdata["Name"] else lang._text("data.null"), 
            age=userdata["Age"] if userdata["Age"] else lang._text("data.null"), 
            bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"), 
            wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),  
            links=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"), 
        ),
        reply_markup=Keybords.keys_open_profile("start.main")
    )

def is_edit_profile(data: types.CallbackQuery):
    if "." in data.data: 
        calldata = data.data.split(".")
        if len(calldata) == 3:
            udata = ".".join([calldata[0], calldata[1]])
            if udata == "profile.edit": return True
    return False

@bot.on_callback_query(lambda orig, data: is_edit_profile(data))
async def edit_profile(origin: Client, data: types.CallbackQuery):
    calldata = data.data.split(".")[2]
    back_keys = Keybords.get_cancel("start.userprofile")

    if calldata == "change_name": text = lang._text("formating_profile_status","edit_predone_profile","text.change_name")
    elif calldata == "change_age": text = lang._text("formating_profile_status","edit_predone_profile","text.change_age")
    elif calldata == "change_bio": text = lang._text("formating_profile_status","edit_predone_profile","text.change_bio")
    elif calldata == "change_wishlist": text = lang._text("formating_profile_status","edit_predone_profile","text.change_wishlist")
    elif calldata == "change_netlinks": text = lang._text("formating_profile_status","edit_predone_profile","text.change_netlinks")
    else: log.warn(f"Not suppoted calldata: {calldata} (is_edit_profile)"); return False

    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.set_userdata_status_type(data.from_user.id, f"profile.edit.{calldata}")
    await data.edit_message_text(
        text=text, 
        reply_markup=back_keys,
        disable_web_page_preview=config.disable_web_page_preview
    )