from Bot.loader import bot, lang, rooms, users, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random
from Defs.keyboard import create_keybord_links

def is_set_name_user_profile(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status == "create_profile":
            return True

    return False

def is_set_name_user_profile(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status == "create_profile":
            return True

    return False

@bot.on_message(lambda orig, msg: is_set_name_user_profile(msg))
async def set_name_create_room(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    status = users.get_user_status_userdata(user_id)

    if len(status) < 5:
        users.add_userdata_status(user_id, msg.text)
    else:
        return False
    
    chat_id, message_id = users.get_messagedata_status(user_id)
    log.debug(status)
    if len(status) == 0:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=lang._text("create_profile","name").format(name=msg.text)
            )
        
        new_message = await msg.reply(
            text=lang._text("create_profile","age", "text.age.edit"),
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.age"
                )
            )
    elif len(status) == 1:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=lang._text("create_profile","age","text.age.new").format(age=msg.text)
            )
        
        new_message = await msg.reply(
            text=lang._text("create_profile","bio","text.bio.new"),
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.age"
                )
            )
    elif len(status) == 2:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=lang._text("create_profile","bio","text.bio.new").format(bio=msg.text)
            )
        
        new_message = await msg.reply(
            text=lang._text("create_profile","wishlist","text.wishilist.edit"),
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.wishlist"
                )
            )
    elif len(status) == 3:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=lang._text("create_profile","wishlist","text.wishlist.new").format(wishlist=msg.text)
            )
        
        new_message = await msg.reply(
            text=lang._text("create_profile","links","text.links.edit"),
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.SocNets"
                )
            )


    elif len(status) == 4:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=lang._text("create_profile","links","text.links.new").format(link=msg.text),
            )
        userdata = users.get_user_status_userdata(msg.from_user.id)
        log.debug(userdata)
        new_message = await msg.reply(
            text=lang._text("create_profile","profile").format(
    name=userdata[0] if userdata[0] else lang._text("data.null"), 
    age=userdata[1] if userdata[1] else lang._text("data.null"), 
    bio=userdata[2] if userdata[2] else lang._text("data.null"), 
    wishlist=userdata[3] if userdata[3] else lang._text("data.null"), 
    links=userdata[4] if userdata[4] else lang._text("data.null"), 
    ),
reply_markup=Keybords.keys_predone_profile())



    users.update_messagedata_status(user_id, new_message.chat.id, new_message.id)