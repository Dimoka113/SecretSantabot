from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random
from datetime import datetime

def is_set_create_room(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status:
            if "create_room" in status.split("."):
                return True

    return False


@bot.on_message(lambda orig, msg: is_set_create_room(msg))
async def set_create_room(origin: Client, msg: types.Message):
    text = msg.text
    user_id = msg.from_user.id
    messagedata = users.get_messagedata_status(user_id)
    status = users.get_messagedata_type(user_id)
    users.add_userdata_status(user_id, text)

    if status == "create_room.name":
        newstatus = "create_room.peer_limit"
        data_edittext = lang._text("nameroom.done")
        edit_text = data_edittext[random.randint(0, len(data_edittext)-1)].format(name=text)
        new_text = lang._text("newroom.peer_limit")
        reply_markup = Keybords.get_skip_and_cancel(
            dir_cancel="cancel.create_room",
            dir_skip="skip.create_room.peer_limit"
            )

        
    elif status == "create_room.peer_limit":
        new_text = lang._text("newroom.room_rule")
        newstatus = "create_room.rules"
        edit_text = lang._text("newroom.peer_limit.done").format(limit=text)
        reply_markup = Keybords.get_skip_and_cancel(
            dir_cancel="cancel.create_room",
            dir_skip="skip.create_room.date_roll"
            )
        
    elif status == "create_room.rules":
        newstatus = "create_room.date_roll"
        new_text = lang._text("newroom.date_roll")
        edit_text = lang._text("newroom.date_roll").format(text=text)
        reply_markup = Keybords.get_datetime_keys_and_cancel(
            dir_cancel="cancel.create_room",
            datenow=datetime.now(),
            daysformats=[15,30,45],
            )

    elif status == "create_room.date_roll":
        newstatus = ""
        edit_text = "Вы указали:\n" + msg.text
        new_text = lang._text("newroom.create_done")

    await bot.edit_message_text(
        chat_id=messagedata[0],
        message_id=messagedata[1],
        text=edit_text
        )
    
    new_message = await msg.reply(
        text=new_text,
        reply_markup=reply_markup
        )
        
    if newstatus:
        users.set_userdata_status_type(user_id, newstatus)
        users.update_messagedata_status(user_id, new_message.chat.id, new_message.id)
    else:
        users.set_clear_user_status(user_id)
        userdata = users.get_user_status_userdata(user_id)
        rooms.create_room(
            name=userdata[0],
            admin_data=[user_id, True],
            peer_limit=userdata[1],
            rule=userdata[2],
            date_created=datetime.now(),
            date_intited=userdata[3],
            date_roll=userdata[3]
        )