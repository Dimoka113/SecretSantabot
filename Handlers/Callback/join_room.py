from Bot.loader import bot, lang, users, rooms, log
from Data import config
from pyrogram import Client, types, filters
from Consts.keyboards import Keybords
from Handlers.Useractions.manually_join_room import selecttype_user_changedata_joinroom


# [[lang._text(self._, "profile.predone.change_name") + save if data[0] else change, "joinroom.manually.change_name"]],
# [[lang._text(self._, "profile.predone.change_age") + save if data[1] else change, "joinroom.manually.change_age"]],
# [[lang._text(self._, "profile.predone.change_bio") + save if data[2] else change, "joinroom.manually.change_bio"]],
# [[lang._text(self._, "profile.predone.change_wishlist") + save if data[3] else change, "joinroom.manually.change_wishlist"]],
# [[lang._text(self._, "profile.predone.change_netlinks") + save if data[4] else change, "joinroom.manually.change_netlinks"]],
# [[lang._text(self._, "room_join_select_done"), "joinroom.manually.done"]],
def is_user_manually_join_room(data: types.CallbackQuery):
    data_list = data.data.split(".")
    if data_list[0] == "joinroom" and data_list[1] == "manually":
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_user_manually_join_room(data))
async def join_manually_room_data(origin: Client, data: types.CallbackQuery):
    user_id = data.from_user.id
    userdata = users.get_user_status_userdata(user_id)

    call = data.data.split(".")[2]

    if call == "change_name":
        userdata[0] = not userdata[0]
    elif call == "change_age":
        userdata[1] = not userdata[1]
    elif call == "change_bio":
        userdata[2] = not userdata[2]
    elif call == "change_wishlist":
        userdata[3] = not userdata[3]
    elif call == "change_netlinks":
        userdata[4] = not userdata[4]
    elif call == "done":
        data_user = users.get_user_by_id(data.from_user.id)

        userdata[0] = data_user["Name"] if userdata[0] else False
        userdata[1] = data_user["Age"] if userdata[1] else False
        userdata[2] = data_user["Bio"] if userdata[2] else False
        userdata[3] = data_user["Wishlist"] if userdata[3] else False
        userdata[4] = data_user["Soc_Nets"] if userdata[4] else False

        log.debug(userdata)
        users.set_userdata_status(user_id, userdata)

        room_id = users.get_messagedata_type(data.from_user.id).split("_")[1]

        new_text = (lang._text("join_room","profile_copy")
                    .format(
                        name = data_user["Name"] if userdata[0] else "",
                        age = data_user["Age"] if userdata[0] else "",
                        bio = data_user["Bio"] if userdata[0] else "",
                        wishlist = data_user["Wishlist"] if userdata[0] else "",
                        links = data_user["Soc_Nets"] if userdata[0] else ""
                        )
        )
        
        await data.message.edit_text(new_text)

        if not userdata[0]:
            new = lang._text("join_room","userdata_naming","text.name")
        elif not userdata[1]:
            new = lang._text("join_room","userdata_naming","text.age")
        elif not userdata[2]:
            new = lang._text("join_room","userdata_naming","text.bio")
        elif not userdata[3]:
            new = lang._text("join_room","userdata_naming","text.wishlist")
        elif not userdata[4]:
            new = lang._text("join_room","userdata_naming","text.links")
        else:
            await data.message.reply("Так как вы выбрали всё, профиль был просто скопирован!")
            rooms.add_user_in_room(room_id, users.get_data_user_by_id(data.from_user.id))
            return True
        message = await data.message.reply(lang._text("join_room","text.message").format(new = new))
        users.update_messagedata_status(user_id, message.chat.id, message.id)
        users.set_userdata_status_type(data.from_user.id, f"joinroom.manually.done_{room_id}")
        return True
    
    users.set_userdata_status(user_id, userdata)
    edit_text = lang._text("join_room","text.edit.copy")
    reply_markup = Keybords.keys_room_change_data(userdata)
    await data.message.edit_text(text=edit_text, reply_markup=reply_markup)


# [[lang._text(self._, "user.join_room.copy_profile"), "joinroom.copy_{room_id}"]],
# [[lang._text(self._, "user.join_room.manual_data"), "joinroom.manually_{room_id}"]],
def is_user_join_room(data: types.CallbackQuery):
    if data.data.split(".")[0] == "joinroom":
        return True
    return False

@bot.on_callback_query(lambda orig, data: is_user_join_room(data))
async def join_room_data(origin: Client, data: types.CallbackQuery):
    userdata = data.data.split(".")[1].split("_")

    if userdata[0] == "copy":
        edit_text = lang._text("join_room","copy")
        rooms.add_user_in_room(userdata[1], users.get_data_user_by_id(data.from_user.id))
        users.add_user_in_room(userdata[1], data.from_user.id)

        await data.message.edit_text(edit_text)
        
    elif userdata[0] == "manually":

        data_add = [True,False,False,False,True]

        users.set_userdata_status_type(data.from_user.id, f"joinroom.manually_{userdata[1]}")
        users.set_userdata_status(data.from_user.id, data_add)
        edit_text = lang._text("join_room","manualy")
        reply_markup = Keybords.keys_room_change_data(data_add)
        await data.message.edit_text(text=edit_text, reply_markup=reply_markup)

    elif userdata[0] == "cancel":
        edit_text = lang._text("join_room","cansel")
        await data.message.edit_text(edit_text)
