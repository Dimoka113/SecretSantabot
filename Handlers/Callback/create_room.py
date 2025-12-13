from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
from datetime import datetime, timedelta

def is_create_room(data: types.CallbackQuery):
    if data.data == "start.createroom": return True
    return False

def is_skip_create_room_peer_limit(data: types.CallbackQuery):
    if data.data == "skip.create_room.peer_limit": return True
    return False

def is_createroom_date_roll(data: types.CallbackQuery):
    spdata = data.data.split(".")
    if spdata[0] == "createroom":
        if spdata[1] == "date_roll":
            return True
    return False



@bot.on_callback_query(lambda orig, data: is_create_room(data))
async def create_room(origin: Client, data: types.CallbackQuery):
    users.set_userdata_status_type(data.from_user.id, "create_room.name")
    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    await data.message.edit_text(
        text=lang._text("newroom.name"), 
        reply_markup=Keybords.get_cancel("cancel.create_room")
        )
    
@bot.on_callback_query(lambda orig, data: is_skip_create_room_peer_limit(data))
async def skip_create_room_peer_limit(origin: Client, data: types.CallbackQuery):
    users.add_userdata_status(data.from_user.id, None)
    users.set_userdata_status_type(data.from_user.id, "create_room.rules")
    await data.message.edit_text(lang._text("newroom.peer_no_limit"))


@bot.on_callback_query(lambda orig, data: is_createroom_date_roll(data))
async def createroom_date_roll(origin: Client, data: types.CallbackQuery):
    spdate = int(data.data.split(".")[2])
    dateform = datetime.now() + timedelta(days=spdate)
    users.add_userdata_status(data.from_user.id, str(dateform))

    messagedata = users.get_messagedata_status(data.from_user.id)

    room_id = rooms.get_random_id()
    reply_markup = Keybords.get_panel_room(room_id, "admin")

    userdata = users.get_user_status_userdata(data.from_user.id)

    new_text = lang._text("newroom.create_done").format(
        name=userdata[0],
        link=f"https://t.me/Secret113Santabot?start={room_id}",
        limit=userdata[1],
        rules=userdata[2],
        date_roll=dateform
        )


    await bot.edit_message_text(
        chat_id=messagedata[0],
        message_id=messagedata[1],
        text=new_text,
        reply_markup=reply_markup
        )
    
    users.add_user_in_room(room_id, data.from_user.id)      
    rooms.create_room(
        id = room_id,
        name=userdata[0],
        admin_data=data.from_user.id,
        peer_limit=userdata[1],
        rule=userdata[2],
        date_created=str(datetime.now()),
        date_intited=userdata[3],
        date_roll=userdata[3]
    )

    users.set_clear_user_status(data.from_user.id)

    await data.message.reply(
        text=lang._text("newroom.is_admin_roll"),
        reply_markup=Keybords.admin_is_roll(room_id)
        )