from Bot.loader import bot, lang, rooms, users
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

@bot.on_message(lambda orig, msg: is_set_name_user_profile(msg))
async def set_name_create_room(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    chat_id, message_id = users.get_messagedata_status(user_id)
    users.add_userdata_status(user_id, msg.text)
    status = users.get_user_status_userdata(user_id)

    print(status)
    if len(status) == 1:
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
    elif len(status) == 2:
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
    elif len(status) == 3:
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
    elif len(status) == 4:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вот что вы хотите:\n{wishlist}".format(wishlist=msg.text)
            )
        
        new_message = await msg.reply(
            text="И последнее, укажите ваши соц сети, чтобы другие игроки знали, как в случае чего с вами связаться\nПример: \"SecretSanta https://t.me/Secret113Santabot\"\n(Вы можете указать сразу несколько соц сетей используйте перенос строки)",
            reply_markup=Keybords.get_skip(
                dir_skip="skip.profile.wishlist"
                )
            )


    elif len(status) == 5:
        media = []
        for link in msg.text.split("\n"):
            info = link.split()
            media.append([[info[0], info[1]]])

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Вот ваши ссылки:",
            reply_markup=create_keybord_links(media)
            )
        
        # ... Добавить сюда функцию, которая вызовет сообщение, такое-же, как для кнопки "Ваш профиль"
        new_message = await msg.reply(
            text="Профиль сформирован!\nПроверьте себя! Если вас всё устраивает, нажмите на кнопку сохранить",
            reply_markup=Keybords.keys_predone_profile()
            )

    users.update_messagedata_status(user_id, new_message.chat.id, new_message.id)