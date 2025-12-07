from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random


def is_set_create_room(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status:
            if "create_room" in status.split("."):
                return True

    return False


@bot.on_message(lambda orig, msg: is_set_create_room(msg))
async def set_create_room(origin: Client, msg: types.Message):
    messagedata = users.get_messagedata_status(msg.from_user.id)
    status = users.get_messagedata_type(msg.from_user.id)
    users.set_userdata_status_type(msg.from_user.id, "create_room.peer_limit")
    user_id = msg.from_user.id
    users.add_userdata_status(user_id, msg.text)

    if status == "create_room.name":
        list_text = lang._text("nameroom.done")
        await bot.edit_message_text(
            chat_id=messagedata[0],
            message_id=messagedata[1],
            text=list_text[random.randint(0, len(list_text)+1)].format(name=msg.text)
            )
        new_message = await msg.reply(
            text=lang._text("newroom.peer_limit"),
            reply_markup=Keybords.get_skip_and_cancel(
                dir_cancel="cancel.create_room",
                dir_skip="skip.create_room.peer_limit"
                )
            )
    elif status == "create_room.peer_limit":



    elif status == "create_room.date_roll":

        await bot.edit_message_text(
            chat_id=messagedata[0],
            message_id=messagedata[1],
            text=lang._text("newroom.peer_limit.done")
            )
        new_message = await msg.reply(
            text=lang._text("newroom.room_rule"),
            reply_markup=Keybords.get_skip_and_cancel(
                dir_cancel="cancel.create_room",
                dir_skip="skip.create_room.peer_limit"
                )
                        )
        
    users.set_userdata_status_type(msg.from_user.id, "create_room.date_roll")

    
    users.update_messagedata_status(msg.from_user.id, new_message.chat.id, new_message.id)