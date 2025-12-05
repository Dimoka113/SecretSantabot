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

def is_skip_profile_age(data: types.CallbackQuery):
    if data.data == "skip.profile.age": return True
    return False

def is_profile_done(data: types.CallbackQuery):
    if data.data == "profile.predone.done": return True
    return False

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


@bot.on_callback_query(lambda orig, data: is_create_profile(data))
async def create_profile_calldata(origin: Client, data: types.CallbackQuery):
    await bot.ed