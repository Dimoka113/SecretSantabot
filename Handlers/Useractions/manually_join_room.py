from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters


def is_select_data_parament(msg: types.Message):
    data_type = users.get_messagedata_type(msg.from_user.id)
    if data_type:
        if data_type.split("_")[0] == "joinroom.manually.done":
            return True
        
    return False

@bot.on_message(lambda orig, msg: is_select_data_parament(msg))
async def selecttype_user_changedata_joinroom(
    origin: Client, msg: types.Message):
    userdata = users.get_user_status_userdata(msg.from_user.id)
    old_msg = users.get_messagedata_status(msg.from_user.id)
    

    if userdata[0] == False: userdata[0] = msg.text; new = "возраст"
    if userdata[1] == False: userdata[1] = msg.text; new = "описание"
    if userdata[2] == False: userdata[2] = msg.text; new = "пожелание"
    if userdata[3] == False: userdata[3] = msg.text; new = "ссылки"
    if userdata[4] == False: userdata[4] = msg.text; new = ""
    else: new = ""
    
    await bot.edit_message_text(chat_id=old_msg[0],
                          message_id=old_msg[1],
                          text=f"Вы указали: {msg.text}"
                          
                          )
    if new:
        new_msg = await msg.reply(f"Теперь укажите {new}")
        users.update_messagedata_status(msg.from_user.id, new_msg.chat.id, new_msg.id)
    else:
        new_data_user = {
            f"{msg.from_user.id}": {
                "Name": userdata[0],
                "Age": userdata[1],
                "Bio": userdata[2],
                "Wishlist": userdata[3],
                "Soc_Nets": userdata[4]
                }
            }
        room_id = users.get_messagedata_type(msg.from_user.id).split("_")[1]
        rooms.add_user_in_room(room_id, new_data_user)
        users.add_user_in_room(room_id, msg.from_user.id)      

        users.set_clear_user_status(msg.from_user.id)
        await msg.reply("Новый профиль успешно сохранён!")