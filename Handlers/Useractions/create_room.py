from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random
from datetime import datetime
from Defs.date_to_text import *


def is_set_create_room(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status:
            if "create_room" in status.split("."):
                return True

    return False


@bot.on_message(lambda orig, msg: is_set_create_room(msg))
async def set_create_room(origin: Client, msg: types.Message):
    if not msg.text:
        return False
    
    text = msg.text
    user_id = msg.from_user.id
    messagedata = users.get_messagedata_status(user_id)
    status = users.get_messagedata_type(user_id)
    userdata = users.get_user_status_userdata(user_id)

    if status == "create_room.name":
        newstatus = "create_room.peer_limit"
        edit_text = lang._text("nameroom.done").format(name=text)
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
        edit_text = lang._text("newroom.rules.done").format(text=text)
        reply_markup = Keybords.get_datetime_keys_and_cancel(
            dir_cancel="cancel.create_room",
            datenow=datetime.now(),
            daysformats=[15,30,45],
            )

    elif status == "create_room.date_roll":
        newstatus = ""
        date_roll = date_text(text, lang._text('months'))
        try:
            edit_text = lang._text("create_room","date").format(date_roll = date_roll)
        except:
            await msg.reply(lang._text("create_room","date.error"))
            return False
        room_id = rooms.get_random_id()
        reply_markup = Keybords.get_panel_room(room_id, "admin")

        new_text = lang._text("newroom.create_done").format(
            name=userdata[0],
            link=lang._text("create_room","room.link"),
            limit=userdata[1],
            rules=userdata[2],
            date_roll=date_roll
            )


    await bot.edit_message_text(
        chat_id=messagedata[0],
        message_id=messagedata[1],
        text=edit_text
        )
    
    new_message = await msg.reply(
        text=new_text,
        reply_markup=reply_markup
        )
        
    users.add_userdata_status(user_id, text)
    if newstatus:
        users.set_userdata_status_type(user_id, newstatus)
        users.update_messagedata_status(user_id, new_message.chat.id, new_message.id)
    else:
        userdata = users.get_user_status_userdata(user_id)
        users.add_user_in_room(room_id, user_id)      
        rooms.create_room(
            id = room_id,
            name=userdata[0],
            admin_data=user_id,
            peer_limit=userdata[1],
            rule=userdata[2],
            date_created=str(datetime.now()),
            date_intited=userdata[3],
            date_roll=userdata[3]
        )

        users.set_clear_user_status(user_id)

        await msg.reply(
            text=lang._text("newroom.is_admin_roll"),
            reply_markup=Keybords.admin_is_roll(room_id)
            )