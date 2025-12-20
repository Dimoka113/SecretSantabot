from Bot.loader import bot, lang, users
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_admin_roll(data: types.CallbackQuery):
# [[lang._text(self._, "emoji_yes"), f"adminroll_yes_{room_id}"]],
# [[lang._text(self._, "emoji_no"), f"adminroll_no_{room_id}"]],
    if data.data.split("_")[0] ==  "adminroll":
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_admin_roll(data))
async def admin_roll(orig: Client, data: types.CallbackQuery):
    _, calldata, room_id  = tuple(data.data.split("_"))

    if calldata == "yes":
        await data.message.edit_text(
            text=lang._text("run_roll","admin","text.message"),
            reply_markup=Keybords.join_room_user_keys(room_id=room_id),
            disable_web_page_preview=config.disable_web_page_preview
        )

    else:
        await data.message.edit_text(
            text=lang._text("run_roll","admin","text.message.edit"),
            disable_web_page_preview=config.disable_web_page_preview
        )
