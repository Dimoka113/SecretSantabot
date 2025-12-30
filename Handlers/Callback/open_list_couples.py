from Bot.loader import bot, lang, users, rooms
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords


# [lang._text(self._, "open_list_couples"), f"openlistcouples_{room_id}"],
def is_open_list_couples(data: types.CallbackQuery):
    if data.data.split("_")[0] == "openlistcouples":
        return True
    
    return False

def is_open_listlistpairs(data: types.CallbackQuery):
    if "listpairs_" in data.data:
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_open_listlistpairs(data))
async def open_listlistpairs_(orig: Client, data: types.CallbackQuery):
    room_id = data.data.split("_")[1]
    text = lang._text("open_list_couples","text.couples_list").format(
        room_name=rooms.get_roomname_by_id(room_id)
        )
    ddict = rooms.get_roolled_by_id(room_id)
    num = 0
    for peer in ddict:
        num = num + 1 
        santa_name = rooms.get_data_user_in_room_id(room_id, peer, "Name")
        sender_name = rooms.get_data_user_in_room_id(room_id, ddict[peer], "Name")
        done_gift = lang._text("open_list_couples", "emoji_done_gift") if rooms.get_messages_in_room_peer(room_id, peer) else ""
        text = (text + lang._text("open_list_couples","text.text").format(
            num=num, 
            santa_name=santa_name, 
            sender_name=sender_name,
            peer=peer,
            ddict=ddict[peer]
            ) + " " + done_gift)
    
    
    
    text = text + (
        lang._text("open_list_couples", "text.couples_list.end")
            .format(
                emoji=lang._text("open_list_couples", "emoji_done_gift")
            )
        )
    await data.message.edit_text(
        text=text,
        disable_web_page_preview=config.disable_web_page_preview,
        reply_markup=Keybords.get_cancel(f"openroom_{room_id}")
    )



@bot.on_callback_query(lambda orig, data: is_open_list_couples(data))
async def open_list_couple(orig: Client, data: types.CallbackQuery):
    room_id = data.data.split("_")[1]
    text = lang._text("open_list_couples","text.couples_list").format(
        room_name=rooms.get_roomname_by_id(room_id)
        )
    ddict = rooms.get_roolled_by_id(room_id)
    num = 0
    for peer in ddict:
        num = num + 1 
        santa_name = rooms.get_data_user_in_room_id(room_id, peer, "Name")
        sender_name = rooms.get_data_user_in_room_id(room_id, ddict[peer], "Name")

        text = text + lang._text("open_list_couples","text.text").format(
            num=num, 
            santa_name=santa_name, 
            sender_name=sender_name,
            peer=peer,
            ddict=ddict[peer]
            ) 
        #f'\n{num}. <a href="tg://user?id={peer}">{santa_name}</a> > <a href="tg://user?id={ddict[peer]}">{sender_name}</a>'

    await data.message.edit_text(
        text=text,
        disable_web_page_preview=config.disable_web_page_preview
    )


