from Bot.loader import bot, lang, rooms, users, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
import random
from Defs.keyboard import create_keybord_links

def is_set_name_user_profile(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status == "create_profile":
            return True

    return False

def is_set_name_user_profile(msg: types.Message):
    if msg.from_user:
        status = users.get_messagedata_type(msg.from_user.id)
        if status == "create_profile":
            return True

    return False

@bot.on_message(lambda orig, msg: is_set_name_user_profile(msg))
async def set_name_create_room(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    status = users.get_user_status_userdata(user_id)

    if len(status) < 5:
        users.add_userdata_status(user_id, msg.text)
    else:
        return False
    
    chat_id, message_id = users.get_messagedata_status(user_id)
    log.debug(status)
    if len(status) == 0:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="{name}? Приятно познакомиться!".format(name=msg.text)
            )
        
        new_message = await msg.reply(
            text="Теперь укажите возраст, который будет у вас в профиле\n(Если вы не хотите, можете пропустить)",
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.age"
                )
            )
    elif len(status) == 1:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Хорошо, вы указали: {age}".format(age=msg.text)
            )
        
        new_message = await msg.reply(
            text="Теперь расскажите немного о себе",
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.age"
                )
            )
    elif len(status) == 2:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вот что вы написали:\n{bio}".format(bio=msg.text)
            )
        
        new_message = await msg.reply(
            text="Теперь расскажите, чего вы желаете? (Так называемый \"вишлист\")",
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.wishlist"
                )
            )
    elif len(status) == 3:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вот что вы хотите:\n{wishlist}".format(wishlist=msg.text)
            )
        
        new_message = await msg.reply(
            text="И последнее, укажите ваши соц сети, чтобы другие игроки знали, как в случае чего с вами связаться",
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.SocNets"
                )
            )


    elif len(status) == 4:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вот ваши ссылки:\n{link}".format(link=msg.text),
            )
        userdata = users.get_user_status_userdata(msg.from_user.id)
        log.debug(userdata)
        new_message = await msg.reply(
            text="""
Профиль сформирован!
————————
Псевдоним: {name}
————————
Возраст: {age}
————————
О себе: 
{bio}
————————
Ваши пожелания: 
{wishlist}
————————
Ваши ссылки: 
{links}
————————
Проверьте себя: Если вас всё устраивает, нажмите на кнопку сохранить
""".format(
    name=userdata[0] if userdata[0] else lang._text("data.null"), 
    age=userdata[1] if userdata[1] else lang._text("data.null"), 
    bio=userdata[2] if userdata[2] else lang._text("data.null"), 
    wishlist=userdata[3] if userdata[3] else lang._text("data.null"), 
    links=userdata[4] if userdata[4] else lang._text("data.null"), 
    ),
reply_markup=Keybords.keys_predone_profile())



    users.update_messagedata_status(user_id, new_message.chat.id, new_message.id)