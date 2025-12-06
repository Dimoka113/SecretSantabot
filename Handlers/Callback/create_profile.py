from Bot.loader import bot, lang, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_create_profile(data: types.CallbackQuery):
    if data.data == "create.userprofile": return True
    return False

def is_skip_profile_age(data: types.CallbackQuery):
    if data.data == "skip.profile.age": return True
    return False

def is_skip_profile_bio(data: types.CallbackQuery):
    if data.data == "skip.profile.bio": return True
    return False

def is_skip_profile_wishlist(data: types.CallbackQuery):
    if data.data == "skip.profile.wishlist": return True
    return False

def is_skip_profile_links(data: types.CallbackQuery):
    if data.data == "skip.profile.links": return True
    return False

def is_back_profile_predone(data: types.CallbackQuery):
    if data.data == "back.profile.predone": return True
    return False

def is_profile_done(data: types.CallbackQuery):
    if data.data == "profile.done": return True
    return False

def is_edit_predone_profile(data: types.CallbackQuery):
    if "." in data.data: 
        calldata = data.data.split(".")
        if len(calldata) == 3:
            udata = ".".join([calldata[0], calldata[1]])
            if udata == "profile.predone": return True
    return False

@bot.on_callback_query(lambda orig, data: is_edit_predone_profile(data))
async def edit_predone_profile(origin: Client, data: types.CallbackQuery):
    calldata = data.data.split(".")[2]
    back_keys = Keybords.get_cancel("back.profile.predone")

    if calldata == "change_name":
        await data.edit_message_text("Хорошо, укажите другой псевдоним", reply_markup=back_keys)
    elif calldata == "change_age":
        await data.edit_message_text("Хорошо, укажите другой возраст", reply_markup=back_keys)
    elif calldata == "change_bio":
        await data.edit_message_text("Хорошо, укажите другое описание", reply_markup=back_keys)
    elif calldata == "change_wishlist":
        await data.edit_message_text("Хорошо, укажите другие ваши предпочтения", reply_markup=back_keys)
    elif calldata == "change_netlinks":
        await data.edit_message_text("Хорошо, укажите другие ваши соц сети", reply_markup=back_keys)


@bot.on_callback_query(lambda orig, data: is_create_profile(data))
async def create_profile_calldata(origin: Client, data: types.CallbackQuery):
    users.add_zero_user(data.from_user.id)
    await data.message.edit_text(text="Хорошо, напишите свой псевдоним")
    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.set_userdata_status_type(data.from_user.id, "create_profile")


@bot.on_callback_query(lambda orig, data: is_skip_profile_age(data))
async def skip_profile_age_calldata(origin: Client, data: types.CallbackQuery):
    await data.message.edit_text(
        text="(Если передумаете, вы всегда можете изменить свой профиль)\nТеперь расскажите немного о себе", 
        reply_markup=Keybords.get_skip(
            dir_skip="skip.profile.bio"
            )
        )
    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.add_userdata_status(data.from_user.id, None)


@bot.on_callback_query(lambda orig, data: is_skip_profile_bio(data))
async def skip_profile_bio_calldata(origin: Client, data: types.CallbackQuery):
    await data.message.edit_text(
        text="(Если передумаете, вы всегда можете изменить свой профиль)\nТеперь расскажите, чего вы желаете", 
        reply_markup=Keybords.get_skip(
            dir_skip="skip.profile.wishlist"
            )
        )
    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.add_userdata_status(data.from_user.id, None)


@bot.on_callback_query(lambda orig, data: is_skip_profile_wishlist(data))
async def skip_profile_wishlist_calldata(origin: Client, data: types.CallbackQuery):
    await data.message.edit_text(
        text="(Если передумаете, вы всегда можете изменить свой профиль)\nПоследнее, укажите ваши соц сети, чтобы другие игроки знали, как в случае чего с вами связаться", 
        reply_markup=Keybords.get_skip(
            dir_skip="skip.profile.links"
            )
        )
    users.update_messagedata_status(data.from_user.id, data.message.chat.id, data.message.id)
    users.add_userdata_status(data.from_user.id, None)

@bot.on_callback_query(lambda orig, data: is_back_profile_predone(data))
@bot.on_callback_query(lambda orig, data: is_skip_profile_links(data))
async def skip_profile_links_calldata(origin: Client, data: types.CallbackQuery):
    if data.data != "back.profile.predone":
        users.add_userdata_status(data.from_user.id, None)
    userdata = users.get_user_status_userdata(data.from_user.id)
    
    await data.edit_message_text(
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



@bot.on_callback_query(lambda orig, data: is_profile_done(data))
async def create_profile_calldata(origin: Client, data: types.CallbackQuery):
    userdata = users.get_user_status_userdata(data.from_user.id)
    
    users.add_user(
        user_id=data.from_user.id, 
        name=userdata[0],
        age=userdata[1],
        bio=userdata[2],
        wishlist=userdata[3],
        soc_networks=userdata[4]
        )
    
    await data.edit_message_text(
        text="Теперь вы можете создать свою комнату:", 
        reply_markup=Keybords.get_start_no_room()
        )
    users.set_clear_user_status(data.from_user.id)