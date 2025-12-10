from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

@bot.on_message(filters.command(commands="start", prefixes=["/", "!"]))
async def start_command(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    if len(msg.text.split()) == 1:
        if users.is_users_exist(user_id):
            await msg.reply(text=lang._text("start_message"), reply_markup=Keybords.get_start_no_room())
        else:
            await msg.reply(text=lang._text("start_message_noprofile"), reply_markup=Keybords.create_profile())

    else:
        if users.is_users_exist(user_id):
            room_id = msg.text.split()[1]
            admin_id = rooms.get_admins_by_id(room_id=room_id)
            if admin_id == user_id:
                await msg.reply(
                    text=lang._text("user.join_room.admin_room").format(name=rooms.get_roomname_by_id(room_id=room_id)),

                    )
                return False
            elif user_id in rooms.get_users_room_by_room_id(room_id):
                await msg.reply(
                    text=lang._text("user.join_room.already").format(name=rooms.get_roomname_by_id(room_id=room_id)),
                    )
                return False
            else:
                await msg.reply(
                    text=lang._text("join_message").format(name=rooms.get_roomname_by_id(room_id=room_id)), 
                    reply_markup=Keybords.join_room_user_keys(room_id=room_id)
                    )
        else:
            users.add_zero_user(user_id)
            users.set_status_origin(user_id, msg.text.split()[1])
            await msg.reply(text=lang._text("join_message_noprofile"), reply_markup=Keybords.create_profile())