from Bot.loader import bot, lang, rooms, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords

@bot.on_message(filters.command(commands="profile", prefixes=["/", "!"]))
async def start_command(origin: Client, msg: types.Message):
    user_id = msg.from_user.id
    if users.is_users_exist(user_id):
        userdata = users.get_user_by_id(user_id)
        await msg.reply(
            text = lang._text("formating_profile_status","profile")
    .format(
        name=userdata["Name"] if userdata["Name"] else lang._text("data.null"), 
        age=userdata["Age"] if userdata["Age"] else lang._text("data.null"), 
        bio=userdata["Bio"] if userdata["Bio"] else lang._text("data.null"), 
        wishlist=userdata["Wishlist"] if userdata["Wishlist"] else lang._text("data.null"),  
        links=userdata["Soc_Nets"] if userdata["Soc_Nets"] else lang._text("data.null"), 
        ),
        reply_markup=Keybords.keys_open_profile("start.main"),
        disable_web_page_preview=config.disable_web_page_preview
    )
    else:
        await msg.reply(
            text=lang._text("start_message_noprofile"), 
            reply_markup=Keybords.create_profile(),
            disable_web_page_preview=config.disable_web_page_preview
            )
