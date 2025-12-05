from Defs.keyboard import create_keybord
from Bot.loader import lang


class Keybords(object):
    _ = "keybords"

    @classmethod
    def get_start(self): return create_keybord(
        [
            [[lang._text(self._, "start.createroom.key_text"), "start.createroom"]],
            [[lang._text(self._, "start.userrooms.key_text"), "start.userrooms"]],
            [[lang._text(self._, "start.userprofile.key_text"), "start.userprofile"]],
            
        ])
    
    @classmethod
    def get_cancel(self, dir_cancel: str): return create_keybord(
        [
            [[lang._text(self._, "back.key.text"), dir_cancel]],
        ])

    @classmethod
    def get_skip_and_cancel(self, dir_cancel: str, dir_skip: str): 
        return create_keybord(
        [
            [[lang._text(self._, "back.key.text"), dir_skip]],
            [[lang._text(self._, "cancel.key.text"), dir_cancel]],
        ])

    class Profile(object):
        _ = "profile"


        

