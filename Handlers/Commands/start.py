from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

@bot.on_message(filters.command(commands="start", prefixes=["/", "!"]))
async def start_command(origin: Client, msg: types.Message):
    if len(msg.text.split()) == 1:
        await msg.reply(text=lang._text("start_message"), reply_markup=Keybords.get_start())
    else:
        room_id = msg.text.split()[1]
        rooms.add_user_in_room(room_id, msg.from_user.id)

        await msg.reply(text=lang._text("join_message").format(name=rooms.get_roomname_by_id(room_id=room_id)))