from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random


def is_set_name_create_room(msg: types.Message):
    if msg.from_user:
        status = users.get_user_status(msg.from_user.id)
        if status:
            if status[0][0] == "create_room":
                return True

    return False

def is_set_user_limit_create_room(msg: types.Message):
    if msg.from_user:
        status = users.get_user_status(msg.from_user.id)
        if status:
            if status[0][0] == "create_room":
                if len(status[0]) == 2: 
                    return True

    return False


@bot.on_message(lambda orig, msg: is_set_name_create_room(msg))
async def set_name_create_room(origin: Client, msg: types.Message):
    status, chat_id, message_id = tuple(users.get_user_status(msg.from_user.id))
    user_id = msg.from_user.id
    users.set_add_user_status(user_id, msg.text)
    list_text = lang._text("nameroom.done")
    
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=list_text[random.randint(0, len(list_text)+1)].format(name=msg.text)
        )
    await msg.reply(
        text=lang._text("newroom.peer_limit"),
        reply_markup=Keybords.get_skip_and_cancel(
            dir_cancel="cancel.create_room",
            dir_skip="skip.create_room.peer_limit"
            )
        )
    

@bot.on_message(lambda orig, msg: is_set_user_limit_create_room(msg))
async def set_user_limit_create_room(origin: Client, msg: types.Message):
    status, chat_id, message_id = tuple(users.get_user_status(msg.from_user.id))
    
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=lang._text("newroom.peer_limit.done")
        )
    await msg.reply(
        text=lang._text("newroom.room_rule"),
        reply_markup=Keybords.get_skip_and_cancel(
            dir_cancel="cancel.create_room",
            dir_skip="skip.create_room.peer_limit"
            )
                    )
