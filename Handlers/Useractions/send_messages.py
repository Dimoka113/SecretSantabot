from Bot.loader import bot, lang, rooms, users, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_predone_send_message(msg: types.Message):
    content = users.get_messagedata_type(msg.from_user.id)
    if content:
        if ("sendmessagee" in content): 
            return True
        
@bot.on_deleted_messages()
async def on_delete_send_message(origin: Client, data: list[types.Message]):
    for mes in data:
        user_id = users.remove_temp_message_by_id(mes.id)
        if user_id:
            user_type = users.get_messagedata_type(user_id)
            userdata = users.get_user_status_userdata(user_id)
            message_data = users.get_messagedata_status(user_id)
            _, room_id, played = user_type.split("_")
            keys_data = Keybords.get_keys_send_gift_users(room_id, played, f"cancel.{_}_{room_id}_{played}")
            await bot.edit_message_text(
                chat_id=message_data[0],
                message_id=message_data[1],
                text=(
                        lang._text("text.send_gift").format(
                        gifter_name=rooms.get_data_user_in_room_id(room_id, played, "Name"))
                        + "\n" 
                        + lang._text("text.message.sended.len").format(lenn=len(userdata)) 
                        +"\n" 
                        + lang._text("text.mention.send_gift")
                     ), 
                reply_markup=keys_data,
                disable_web_page_preview=config.disable_web_page_preview
            )
        

@bot.on_message(lambda orig, msg: is_predone_send_message(msg))
async def selecttype_user_changedata_joinroom(
    origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    
    if msg.media_group_id:
        if not users.check_media_group_exist(user_id, msg.media_group_id):
            users.add_userdata_status(user_id, [msg.chat.id, msg.id, msg.media_group_id])
        else:
            return "Media Exist"
    else:
        users.add_userdata_status(user_id, [msg.chat.id, msg.id])

    user_type = users.get_messagedata_type(user_id)
    userdata = users.get_user_status_userdata(user_id)
    message_data = users.get_messagedata_status(user_id)
    _, room_id, played = user_type.split("_")

    await bot.edit_message_text(
        chat_id=message_data[0],
        message_id=message_data[1],
        text=
            (
                lang._text("text.send_gift").format(
                gifter_name=rooms.get_data_user_in_room_id(room_id, played, "Name"))
                + "\n" 
                + lang._text("text.message.sended.len").format(lenn=len(userdata)) 
                +"\n" 
                + lang._text("text.mention.send_gift")
            ), 
        reply_markup=Keybords.get_keys_send_gift_users(room_id, played, f"cancel.{_}_{room_id}_{played}"),
        disable_web_page_preview=config.disable_web_page_preview
    )
