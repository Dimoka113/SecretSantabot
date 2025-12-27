from Defs.keyboard import create_keybord
from Bot.loader import lang
from pyrogram import types
from datetime import datetime, timedelta

class Keybords(object):
    _ = "keybords"

    @classmethod
    def get_start_all(self) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "start.createroom.key_text"), "start.createroom"]],
            [[lang._text(self._, "start.userrooms.key_text"), "start.userrooms"]],
            [[lang._text(self._, "start.userprofile.key_text"), "start.userprofile"]],
            
        ])
    
    @classmethod
    def get_start_no_room(self) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "start.createroom.key_text"), "start.createroom"]],
            [[lang._text(self._, "start.userprofile.key_text"), "start.userprofile"]],
            
        ])
    
    @classmethod
    def create_profile(self) -> types.InlineKeyboardMarkup:  
        return create_keybord(
        [
            [[lang._text(self._, "create.userprofile.key_text"), "create.userprofile"]],
        ])

    @classmethod
    def get_cancel(self, dir_cancel: str) -> types.InlineKeyboardMarkup:
        return create_keybord(
        [
            [[lang._text(self._, "back.key.text"), dir_cancel]],
        ])

    @classmethod
    def get_skip(self, dir_skip: str) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "skip.key.text"), dir_skip]],
        ])

    @classmethod
    def keys_predone_profile(self) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "profile.predone.change_name"), "profile.predone.change_name"]],
            [[lang._text(self._, "profile.predone.change_age"), "profile.predone.change_age"]],
            [[lang._text(self._, "profile.predone.change_bio"), "profile.predone.change_bio"]],
            [[lang._text(self._, "profile.predone.change_wishlist"), "profile.predone.change_wishlist"]],
            [[lang._text(self._, "profile.predone.change_netlinks"), "profile.predone.change_netlinks"]],
            [[lang._text(self._, "profile.done"), "profile.done"]],
        ])
    
    @classmethod
    def keys_room_change_data(self, data: list) -> types.InlineKeyboardMarkup: 
        save = lang._text("emoji_save")
        change = lang._text("emoji_change")

        return create_keybord(
        [
            [[lang._text(self._, "profile.predone.change_name") + (save if data[0] else change), "joinroom.manually.change_name"]],
            [[lang._text(self._, "profile.predone.change_age") + (save if data[1] else change), "joinroom.manually.change_age"]],
            [[lang._text(self._, "profile.predone.change_bio") + (save if data[2] else change), "joinroom.manually.change_bio"]],
            [[lang._text(self._, "profile.predone.change_wishlist") + (save if data[3] else change), "joinroom.manually.change_wishlist"]],
            [[lang._text(self._, "profile.predone.change_netlinks") + (save if data[4] else change), "joinroom.manually.change_netlinks"]],
            [[lang._text(self._, "room_join_select_done"), "joinroom.manually.done"]],
        ])

    @classmethod
    def keys_open_profile(self, dir_cancel: str) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "profile.predone.change_name"), "profile.edit.change_name"]],
            [[lang._text(self._, "profile.predone.change_age"), "profile.edit.change_age"]],
            [[lang._text(self._, "profile.predone.change_bio"), "profile.edit.change_bio"]],
            [[lang._text(self._, "profile.predone.change_wishlist"), "profile.edit.change_wishlist"]],
            [[lang._text(self._, "profile.predone.change_netlinks"), "profile.edit.change_netlinks"]],
            [[lang._text(self._, "back.key.text"), dir_cancel]],
        ])
    
    @classmethod
    def keys_open_profile_in_room(self, room_id: str, dir_cancel: str) -> types.InlineKeyboardMarkup: 
        return create_keybord(
        [
            [[lang._text(self._, "profile.predone.change_name"), f"dataroom.edit_{room_id}.change_name"]],
            [[lang._text(self._, "profile.predone.change_age"), f"dataroom.edit_{room_id}.change_age"]],
            [[lang._text(self._, "profile.predone.change_bio"), f"dataroom.edit_{room_id}.change_bio"]],
            [[lang._text(self._, "profile.predone.change_wishlist"), f"dataroom.edit_{room_id}.change_wishlist"]],
            [[lang._text(self._, "profile.predone.change_netlinks"), f"dataroom.edit_{room_id}.change_netlinks"]],
            [[lang._text(self._, "back.key.text"), dir_cancel]],
        ])
    
    @classmethod
    def get_skip_and_cancel(self, dir_cancel: str, dir_skip: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
        [
            [[lang._text(self._, "skip.key.text"), dir_skip]],
            [[lang._text(self._, "cancel.key.text"), dir_cancel]],
        ])

    @classmethod
    def get_datetime_keys_and_cancel(self, dir_cancel: str, datenow: datetime, daysformats: list[int]) -> types.InlineKeyboardMarkup: 
        keys = []
        for date in daysformats:
            dateform = datenow + timedelta(days=date)
            keys.append([[dateform, f"createroom.date_roll.{date}"]])

        return create_keybord(keys)
    
    
    @classmethod
    def get_list_rooms(self, room_ids: list[list[str]]) -> types.InlineKeyboardMarkup: 
        i = [
                [[i[1], f"openroom_{i[0]}"]] for i in room_ids
            ]
        i.append([[lang._text(self._, "back.key.text"), "start"]]) 
        return create_keybord(i)


    
    @classmethod
    def get_panel_room(self, room_id: str, user_perm: str, dir_cancel: str = None):
        """
        #### `user_perm` can be: 
        ```["participant", "comadmin", "admin"]
        """

        if user_perm == "admin":
            return create_keybord(
            [
                [[lang._text(self._, "rooms", "list_users"), f"listusers_{room_id}"]],
                [[lang._text(self._, "rooms", "list_pairs"), f"listpairs_{room_id}"]],
                [[lang._text(self._, "rooms", "start_action"), f"startaction_{room_id}"]],
                [[lang._text(self._, "rooms", "user_data"), f"userdata_{room_id}"]],
                [[lang._text(self._, "rooms", "gift_user"), f"giftuser_{room_id}"]],
                [[lang._text(self._, "open.settings_room"), f"settingsroom_{room_id}"]],
                [[lang._text(self._, "back.key.text"), dir_cancel]],
            ])
        
        elif user_perm == "participant":
            return create_keybord(
            [
                [[lang._text(self._, "rooms", "list_users"), f"listusers_{room_id}"]],
                [[lang._text(self._, "rooms", "user_data"), f"userdata_{room_id}"]],
                [[lang._text(self._, "rooms", "gift_user"), f"giftuser_{room_id}"]],
                [[lang._text(self._, "back.key.text"), dir_cancel]],
            ])
        else:
            raise Exception("Do not support!")
        
    @classmethod
    def join_room_user_keys(self, room_id: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
        [
            [[lang._text(self._, "user.join_room.copy_profile"), f"joinroom.copy_{room_id}"]],
            [[lang._text(self._, "user.join_room.manually_data"), f"joinroom.manually_{room_id}"]],
            [[lang._text(self._, "cancel.key.text"), f"joinroom.cancel_{room_id}"]],
        ])

    @classmethod
    def admin_is_roll(self, room_id: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
        [
            [
                [lang._text("emoji_yes"), f"adminroll_yes_{room_id}"],
                [lang._text("emoji_no"), f"adminroll_no_{room_id}"]
            ],
        ])


    @classmethod
    def get_keys_open_user_profile(self, room_id: str, user_id: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [[lang._text(self._, "open_origin_userprofile"), f"openprofile_{room_id}_{user_id}"]],
                [[lang._text(self._, "send_gift"), f"sendmessagee_{room_id}_{user_id}"]],
            ]
        )
    
    @classmethod
    def get_keys_send_gift_users(self, room_id: str, user_id: str, dir_cancel: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [[lang._text(self._, "cancel.key.text"), dir_cancel]],
                [[lang._text(self._, "user.done.gift"), f"senddonemessagee_{room_id}_{user_id}"]],
            ]
        )

    @classmethod
    def get_keys_open_user_profile_back(self, room_id: str, user_id: str, dir_cancel: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [[lang._text(self._, "open_origin_userprofile"), f"back.openprofile_{room_id}_{user_id}"]],
                [[lang._text(self._, "send_gift"), f"sendmessageeback_{room_id}_{user_id}"]],
                [[lang._text(self._, "back.key.text"), dir_cancel]],
            ]
        )

    @classmethod
    def get_keys_open_room_profile_back(self, room_id: str, user_id: str, dir_cancel: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [[lang._text(self._, "open_origin_roombase"), f"back.openroomprofile_{room_id}_{user_id}"]],
                [[lang._text(self._, "send_gift"), f"sendmessageeback_{room_id}_{user_id}"]],
                [[lang._text(self._, "back.key.text"), dir_cancel]],
            ]
        )

    @classmethod
    def get_keys_open_room_profile(self, room_id: str, user_id: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [[lang._text(self._, "open_origin_roombase"), f"openroomprofile_{room_id}_{user_id}"]],
                [[lang._text(self._, "send_gift"), f"sendmessagee_{room_id}_{user_id}"]],
            ]
        )
        
    @classmethod
    def get_list_partient(self, room_id: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
                [
                    [lang._text(self._, "open_list_couples"), f"openlistcouples_{room_id}"],
                ],
            ]
        )
    
    @classmethod
    def get_keys_list_users(self, room_id: str, users: list[int], dir_cancel: str) -> types.InlineKeyboardMarkup:  
        i = [[[i[1], f"open.user_{room_id}_{i[0]}"]] for i in users]
        i.append([[lang._text(self._, "back.key.text"), dir_cancel]]) 
        return create_keybord(i)
    

    @classmethod
    def get_keys_control_user(self, room_id: str, user_id: int, dir_cancel: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
[[lang._text(self._, "users_control", "delete.text"), f"user.delete_{room_id}_{user_id}"]],
[[lang._text(self._, "users_control", "coamin.text"), f"user.coamin_{room_id}_{user_id}"]],
[[lang._text(self._, "users_control", "remove_coadmin.text"), f"user.removecoadmin_{room_id}_{user_id}"]],
[[lang._text(self._, "users_control", "transfer.admin.text"), f"user.transfer_{room_id}_{user_id}"]],
[[lang._text(self._, "back.key.text"), dir_cancel]],
            ]
        )
    
    @classmethod
    def get_keys_delete_user(self, room_id: str, user_id: int, dir_cancel: str) -> types.InlineKeyboardMarkup:  
        return create_keybord(
            [
[[lang._text(self._, "users_control", "sure.delete.user"), f"user.suredelete_{room_id}_{user_id}"]],
[[lang._text(self._, "back.key.text"), dir_cancel]],
            ]
        )