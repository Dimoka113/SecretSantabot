from Defs.keyboard import create_keybord
from Bot.loader import lang


class Keybords(object):
    _ = "keybords"

    @classmethod
    def get_start(self): return create_keybord(
        [
            [[lang._text(self._, "start.createroom.key_text"), "start.createroom"]],
            [[lang._text(self._, "start.joinroom.key_text"), "start.joinroom"]],
            [[lang._text(self._, "start.userrooms.key_text"), "start.userrooms"]],
            [[lang._text(self._, "start.userprofile.key_text"), "start.userprofile"]],
            
        ])
    

    class Profile(object):
        _ = "profile"


        

