from Bot.loader import bot, lang, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_open_profile(data: types.CallbackQuery):
    if data.data == "start.userprofile": return True
    return False

def is_edit_profile(data: types.CallbackQuery):
    if data.data == "start.main": return True
    return False


@bot.on_callback_query(lambda orig, data: is_open_profile(data))
async def skip_profile_links_calldata(origin: Client, data: types.CallbackQuery):
    userdata = users.get_user_by_id(data.from_user.id)
    await data.edit_message_text(
            text="""
Ваш профиль:
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

Выберите то, что вы хотите изменить:
""".format(
    name=userdata["Name"] if userdata["Name"] else lang._text("data.null"), 
    age=userdata["Age"] if userdata["Age"] else lang._text("data.null"), 
    bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"), 
    wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),  
    links=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"), 
    ),
reply_markup=Keybords.keys_open_profile("start.main")
)


@bot.on_callback_query(lambda orig, data: is_back_profile(data))
async def back_profile(origin: Client, data: types.CallbackQuery):
    await data.edit_message_text(
        text=lang._text("start_message"), 
        reply_markup=Keybords.get_start_no_room()
    )