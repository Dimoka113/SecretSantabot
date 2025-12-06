from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

@bot.on_message(filters.command(commands="start", prefixes=["/", "!"]))
async def start_command(origin: Client, msg: types.Message):
    if len(msg.text.split()) == 1:
        if users.is_users_exist(msg.from_user.id):
            await msg.reply(text=lang._text("start_message"), reply_markup=Keybords.get_start_no_room())
        else:
            await msg.reply(text=lang._text("start_message_noprofile"), reply_markup=Keybords.create_profile())

    else:
        if users.is_users_exist(msg.from_user.id):
            room_id = msg.text.split()[1]
            rooms.add_user_in_room(room_id, msg.from_user.id)

            await msg.reply(text=lang._text("join_message").format(name=rooms.get_roomname_by_id(room_id=room_id)))
        else:
            users.add_zero_user(msg.from_user.id)
            users.set_status_origin
            await msg.reply(text=lang._text("join_message_noprofile"), reply_markup=Keybords.create_profile())