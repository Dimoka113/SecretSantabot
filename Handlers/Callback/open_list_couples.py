from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


# [lang._text(self._, "open_list_couples"), f"openlistcouples_{room_id}"],
def is_open_list_couples(data: types.CallbackQuery):
    if data.data.split("_")[0] == "openlistcouples":
        return True
    
    return False



@bot.on_callback_query(lambda orig, data: is_open_list_couples(data))
async def open_list_couple(orig: Client, data: types.CallbackQuery):
    room_id = data.data.split("_")[1]
    text = lang._text("open_list_couples","text.couples_list").format(room_name=rooms.get_roomname_by_id(room_id))
    ddict = rooms.get_roolled_by_id(room_id)

    num = 0

    for peer in ddict:
        num = num + 1 
        santa_name = rooms.get_data_user_in_room_id(room_id, peer, "Name")
        sender_name = rooms.get_data_user_in_room_id(room_id, ddict[peer], "Name")

        text = text + lang._text("open_list_couples","text.text").format(num = num, santa_name = santa_name, sender_name = sender_name) 
        #f'\n{num}. <a href="tg://user?id={peer}">{santa_name}</a> > <a href="tg://user?id={ddict[peer]}">{sender_name}</a>'

    await data.message.edit_text(
        text=text
    )


