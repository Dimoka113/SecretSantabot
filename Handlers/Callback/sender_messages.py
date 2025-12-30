from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
from datetime import datetime

def is_cancel_send_messages(data: types.CallbackQuery):
    if "cancel.sendmessagee" in data.data:
        return True
    return False

@bot.on_callback_query(lambda origin, data: is_cancel_send_messages(data))
async def cancel_update_data_to_send_messages(orig: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id, played = data.data.split("_")
    users.set_clear_user_status(user_id)


    rolled = rooms.get_roolled_by_id(room_id)
    if rolled:
        played = rolled[str(user_id)]
        try:
            played_data = await bot.get_chat(played)
            played_username_text = f"(@{played_data.username})" if played_data.username else ""
        except:
            played_username_text= ""

        await data.message.edit(
            text=lang._text("run_roll","text.message_private").format(
                name =rooms.get_data_user_in_room_id(room_id, played, "Name"),
                played = played, 
                played_username_text = played_username_text
            ),
            reply_markup=Keybords.get_keys_open_user_profile_back(room_id, played, f"openroom_{room_id}"),
            disable_web_page_preview=config.disable_web_page_preview
        )
    else:
        await data.answer(
            text=lang._text("roll.donot_runned.message"), 
            show_alert=True
        )

def is_done_send_messages(data: types.CallbackQuery):
    if "senddonemessagee" in data.data:
        return True
    return False

@bot.on_callback_query(lambda origin, data: is_done_send_messages(data))
async def cancel_update_data_to_send_messages(orig: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    _, room_id, played = data.data.split("_")
    date = datetime.now()
    user_data = users.get_user_status_userdata(user_id)
    message_data = users.get_messagedata_status(user_id)
    if len(user_data) == 0:
        await data.answer(lang._text("user.not.send_messages"))
        return False
    else:
        rooms.white_new_message_gift(room_id, date, user_id, user_data)
        users.set_clear_user_status(user_id)

        await bot.edit_message_text(
            chat_id=message_data[0],
            message_id=message_data[1],
            text=lang._text("text.message.send_origin"),
        )
        for message in user_data:
            if len(message) == 3:
                messages = await bot.get_media_group(message[0], message[1])
                medias = []
                for message in messages:
                    if message.video: 
                        medias.append(
                            types.InputMediaVideo(
                                media=message.video.file_id,
                                thumb=message.video.thumbs[0].file_id,
                                caption=message.caption,
                                caption_entities=message.caption_entities,
                                width=message.video.width,
                                height=message.video.height,
                                duration=message.video.duration,
                                file_name=message.video.file_name,
                                supports_streaming=message.video.supports_streaming,
                                has_spoiler=message.has_media_spoiler,
                            )
                        )
                        
                    elif message.audio: 
                        medias.append(
                            types.InputMediaAudio(
                                media=message.audio.file_id,
                                thumb=message.audio.thumbs[0].file_id,
                                caption=message.caption,
                                caption_entities=message.caption_entities,
                                duration=message.audio.duration,
                                file_name=message.audio.file_name,
                                performer=message.audio.performer,
                                title=message.audio.title
                            )
                        )
                    elif message.photo: 
                        medias.append(
                            types.InputMediaPhoto(
                                media=message.photo.file_id,
                                caption=message.caption,
                                caption_entities=message.caption_entities,
                                has_spoiler=message.has_media_spoiler,
                            )
                        )
                    elif message.document: 
                        medias.append(
                            types.InputMediaDocument(
                                media=message.document.file_id,
                                thumb=message.document.thumbs[0].file_id,
                                caption=message.caption,
                                caption_entities=message.caption_entities,
                                file_name=message.document.file_name,
                            )
                        )


                await bot.send_media_group(played, medias)
            else:
                await bot.copy_message(played, message[0], message[1])
            await bot.send_message(played, lang._text("text.on_reply_gift"))

def is_send_messages(data: types.CallbackQuery):
    if "sendmessagee" in data.data:
        return True
    return False


@bot.on_callback_query(lambda origin, data: is_send_messages(data))
async def update_data_to_send_messages(orig: Client, data: types.CallbackQuery):
    _, room_id, played = data.data.split("_")
    
    back_keys = Keybords.get_keys_send_gift_users(room_id, played, f"cancel.{_}_{room_id}_{played}")

    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.set_userdata_status_type(data.from_user.id, data.data)
    await data.edit_message_text(
        text=lang._text("text.send_gift").format(
            gifter_name=rooms.get_data_user_in_room_id(room_id, played, "Name")
        ) + "\n\n" + lang._text("text.mention.send_gift"), 
        reply_markup=back_keys,
        disable_web_page_preview=config.disable_web_page_preview
    )
