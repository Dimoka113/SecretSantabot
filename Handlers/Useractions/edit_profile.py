from Bot.loader import bot, lang, rooms, users, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random
from Defs.keyboard import create_keybord_links

# [[lang._text(self._, "profile.predone.change_name"), "profile.predone.change_name"]],
# [[lang._text(self._, "profile.predone.change_age"), "profile.predone.change_age"]],
# [[lang._text(self._, "profile.predone.change_bio"), "profile.predone.change_bio"]],
# [[lang._text(self._, "profile.predone.change_wishlist"), "profile.predone.change_wishlist"]],
# [[lang._text(self._, "profile.predone.change_netlinks"), "profile.predone.change_netlinks"]],

# [[lang._text(self._, "profile.predone.change_name"), "profile.edit.change_name"]],
# [[lang._text(self._, "profile.predone.change_age"), "profile.edit.change_age"]],
# [[lang._text(self._, "profile.predone.change_bio"), "profile.edit.change_bio"]],
# [[lang._text(self._, "profile.predone.change_wishlist"), "profile.edit.change_wishlist"]],
# [[lang._text(self._, "profile.predone.change_netlinks"), "profile.edit.change_netlinks"]],
# [[lang._text(self._, "back.key.text"), dir_cancel]],

def is_edit_profile_content(msg: types.Message):
    content = users.get_messagedata_type(msg.from_user.id).split(".")
    if (len(content) > 1 and content[0] == "profile" and content[1] == "edit"): 
        return True

def is_edit_predone_profile_content(msg: types.Message):
    content = users.get_messagedata_type(msg.from_user.id).split(".")
    if (len(content) > 1 and content[0] == "create_profile" and content[1] == "edit"): 
        return True
    

@bot.on_message(lambda orig, data: is_edit_profile_content(data))
async def predone_edit_profile_content(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    content = users.get_messagedata_type(user_id).split(".")
    messagedata = users.get_messagedata_status(user_id)
    if content[2] == "change_name": datatype = "Name"
    elif content[2] == "change_age": datatype = "Age"
    elif content[2] == "change_bio": datatype = "Bio"
    elif content[2] == "change_wishlist": datatype = "Wishlist"
    elif content[2] == "change_netlinks": datatype = "Soc_Nets"
    else: log.warn(f"Not supported datatype {content} (is_edit_profile_content)"); return False

    users.set_clear_user_status(user_id)
    users.change_meta_user_by_id(msg.from_user.id, datatype, msg.text)
    userdata = users.get_user_by_id(msg.from_user.id)
    await bot.edit_message_text(
        chat_id=messagedata[0],
        message_id=messagedata[1],
        text=lang._text("formating_profile_status","profile").format(
    name=userdata["Name"] if userdata["Name"] else lang._text("data.null"), 
    age=userdata["Age"] if userdata["Age"] else lang._text("data.null"), 
    bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"), 
    wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),  
    links=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"), 
    ),
reply_markup=Keybords.keys_open_profile("start.main")
)
    

@bot.on_message(lambda orig, data: is_edit_predone_profile_content(data))
async def predone_edit_profile_content(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    content = users.get_messagedata_type(user_id).split(".")
    messagedata = users.get_messagedata_status(user_id)
    data = users.get_user_status_userdata(user_id)

    if content[2] == "change_name": i = 0
    elif content[2] == "change_age": i = 1
    elif content[2] == "change_bio": i = 2 
    elif content[2] == "change_wishlist": i = 3
    elif content[2] == "change_netlinks": i = 4
    else: log.warn(f"Not supported datatype {content} (is_edit_profile_content)"); return False
    
    data[i] = msg.text
    users.set_userdata_status(user_id, data)
    userdata = users.get_user_status_userdata(user_id)
    
    await bot.edit_message_text(
        chat_id=messagedata[0], message_id=messagedata[1],
            text=lang._text("create_profile","profile").format(
    name=userdata[0] if userdata[0] else lang._text("data.null"), 
    age=userdata[1] if userdata[1] else lang._text("data.null"), 
    bio=userdata[2] if userdata[2] else lang._text("data.null"), 
    wishlist=userdata[3] if userdata[3] else lang._text("data.null"), 
    links=userdata[4] if userdata[4] else lang._text("data.null"), 
    ),
reply_markup=Keybords.keys_predone_profile())
