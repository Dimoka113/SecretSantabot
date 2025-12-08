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
            keys.append([[dateform, f"dateroom_{'-'.join(str(date).split())}"]])


        keys.append([[lang._text(self._, "cancel.key.text"), dir_cancel]])
        return create_keybord(keys)
    

