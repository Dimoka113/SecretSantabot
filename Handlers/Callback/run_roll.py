from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


def is_start_runroll(data: types.CallbackQuery):
    if data.data.split("_")[0] == "startaction":
        return True
    return False




@bot.on_callback_query(lambda orig, data: is_start_runroll(data))
async def start_runroll(orig: Client, data: types.CallbackQuery):

    room_id = data.data.split("_")[1]

    rooms.run_roll_in_room_id(room_id=room_id)
    ddict = rooms.get_roolled_by_id(room_id)
    await data.message.reply(
        text=f"Ручная жеребьёвка произошла, нажмите, чтобы посмотреть список пар:", 
        reply_markup=Keybords.get_list_partient(room_id=room_id)
        
        )

    for user_id in ddict:

        played = ddict[user_id]
        log.debug(str(user_id) + " > " + str(played))
        try:
            played_data = await bot.get_chat(played)
            played_username_text = f"(@{played_data.username})" if played_data.username else ""
        except:
            played_username_text= ""

        try:
            await bot.send_message(
    chat_id=int(user_id), 
    text=f'''Ты Тайный Санта для: <a href="tg://user?id={played}">{rooms.get_data_user_in_room_id(room_id, played, "Name")}</a>''' 
    + played_username_text

    + '''\nБудем ждать, что же ты ему подаришь!''',
    reply_markup=Keybords.get_keys_open_user_profile(room_id, played)
                )
        except:
            pass