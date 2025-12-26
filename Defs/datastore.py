import json, os, asyncio
from Defs.random_id import get_random_id
from datetime import datetime
from Defs.roll_users import *
from pyrogram import types, Client
from Defs.logger import Logger


class DataBot(object):
    logger = None
    id = int()
    is_deleted = bool()    
    is_frozen = bool()      
    is_bot = bool()
    is_verified = bool()
    is_premium = bool()
    first_name = str()
    username = str()
    dc_id = int(),

    def __init__(self, logger: Logger):
        self.logger = logger

    async def update_bot(self, bot: Client) -> bool:
        try:
            data = await bot.get_me()
            self.id = data.id
            self.is_deleted = data.is_deleted
            self.is_frozen = data.is_frozen    
            self.is_bot = data.is_bot
            self.is_verified = data.is_verified
            self.is_premium = data.is_premium
            self.first_name = data.first_name
            self.username = data.username
            self.dc_id = data.dc_id
        except:
            self.logger.crit(
"We couldn't get the bot info. Did you make sure you put in the right details?"
                )
            return False
        else:
            return True

class Gateway(object):
    path = str()
    def __init__(self, path: str):
        self.path = path
        if not self.check_exist():
            with open(self.path, "w+", encoding="UTF-8") as file: 
                json.dump({}, file, indent=3, ensure_ascii=False)

    def check_exist(self): return os.path.isfile(path=self.path)

    def read(self) -> dict:
        with open(self.path, "r", encoding="UTF-8") as file: 
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as err:
                from Bot.loader import log
                log.warn(err)
                return {}

    def white(self, data: dict) -> bool:
        """
Returns `True` if successful.

If unsuccessful, outputs a log with `WARN` and returns `False`.
        """
        try: 
            with open(self.path, "w", encoding="UTF-8") as file: json.dump(data, file, indent=3, ensure_ascii=False)
        except Exception as err:
            from Bot.loader import log
            log.warn(err)
            return False
        else: return True


class Rooms(Gateway):
    get_random_id = staticmethod(get_random_id)
    def __init__(self, path): 
        super().__init__(path)
    

    def create_room(self, 
    id: str,
    name: str, 
    admin_data: int,
    peer_limit: int, 
    rule: str,   # Условие обмена
    date_created: datetime, # Время, когда комната была создана
    date_intited: datetime, # Время, когда больше нельзя будет заходить в комнату, и её настраивать
    date_roll: datetime,    # Время, когда запуститься жеребьёвка
                    ):
        data = self.read()
        data[id] = {
        "name": name,
        "admin": admin_data,
        "rule": rule,
        "is_open": True,
        "peer_limit": int(peer_limit) if peer_limit else peer_limit,
        "date_created": date_created,
        "date_intited": date_intited,
        "date_roll": date_roll,
        "coadmins": [],
        "users": {},
        "roll": {},
        }
        return self.white(data)
        # ...

    def add_user_in_room(self, room_id: str, user_data: dict) -> bool:
        data = self.read()
        data[room_id]["users"].update(user_data)

        return self.white(data)


    def run_roll_in_room_id(self, room_id: str):
        data = self.read()
        
        data[str(room_id)]["roll"] = roll_users(self.get_users_room_by_room_id(room_id))

        return self.white(data)

    def get_roolled_by_id(self, room_id: str) -> dict:
        return self.read()[str(room_id)]["roll"]
    

    def delete_user_in_room(self, room_id: str, user_id: int|str) -> bool:
        data = self.read()
        del data[room_id]["users"][str(user_id)]
        return self.white(data)

    def get_roomname_by_id(self, room_id: str) -> str:
        return self.read()[str(room_id)]["name"]
    
    def get_rules_by_id(self, room_id: str) -> str:
        return self.read()[str(room_id)]["rule"]
    
    def get_peer_limit_by_id(self, room_id: str) -> str:
        return self.read()[str(room_id)]["peer_limit"]
    
    def get_date_roll_by_id(self, room_id: str) -> str:
        return self.read()[str(room_id)]["date_roll"]
    
    def get_admins_by_id(self, room_id: str) -> int:
        return int(self.read()[str(room_id)]["admin"])

    def get_rooms(self) -> list[str]:
        return [i for i in self.read()]

    def delete_room(self, room_id: str) -> bool:
        data = self.read()
        del data[str(room_id)]
        return self.white(data)
    
    def get_users_room_by_room_id(self, room_id: str) -> list:
        data = self.read()
        return [int(i) for i in data[str(room_id)]["users"]]
    
    def get_number_users_in_room(self, room_id: str) -> int:
        return len(self.read()[str(room_id)]["users"])
    
    def get_data_user_in_room_id(self, room_id: str, user_id: str, data: str = None) -> dict|str:
        if data:
            return self.read()[str(room_id)]["users"][str(user_id)][data]
        else:
            return self.read()[str(room_id)]["users"][str(user_id)]

    def set_data_user_in_room_id(self, room_id: str, user_id: str, content: dict|str, data: str = None) -> dict|str:
        userdata = self.read()
        if data: userdata[str(room_id)]["users"][str(user_id)][data] = content
        else: userdata[str(room_id)]["users"][str(user_id)] = content
        return self.white(userdata)
    
class Hide_id(Gateway):
    def __init__(self, path): 
        super().__init__(path)

    def check_exist_data(self):
        data = self.read()
        try:
            if data["list_ids"]: return True
        except:
            data["list_ids"] = []
            if not self.white(data):
                raise("Error write")
            return False
        else:
            return True

    def check_by_id(self, user_id: int|str) -> bool:
        return int(user_id) in self.read()["list_ids"]

    def get_user_id(self, random_id: str) -> int:
        return int(self.read()[random_id])
    
    def set_random_id(self, user_id: int | str) -> bool:
        data = self.read()
        data[get_random_id(user_id)] = str(user_id)
        data["list_ids"].append(int(user_id))
        return self.white(data)

class Users(Gateway):
    def __init__(self, path): 
        super().__init__(path)

    def add_zero_user(self, user_id: int):
        data = self.read()
        data[str(user_id)] = {"status": {"type": "", "origin": "", "messagedata": [], "userdata": []}, "rooms": []}
        return self.white(data)
    
    def is_users_exist(self, user_id: int) -> bool:
        return bool(str(user_id) in self.read())

    def get_user_status_userdata(self, user_id: int) -> list|None:
        if self.is_users_exist(user_id):
            return self.read()[str(user_id)]["status"]["userdata"]
        else:
            return None
        
    def get_messagedata_status(self, user_id: int) -> list:
        data = self.read()
        return data[str(user_id)]["status"]["messagedata"]
    
    def get_messagedata_type(self, user_id: int) -> str|None:
        data = self.read()
        try: return data[str(user_id)]["status"]["type"]
        except: return None
        
    def set_status_origin(self, user_id: int, origin: str) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["origin"] = origin
        return self.white(data)

    def update_messagedata_status(self, user_id: int, chat_id: int, msg_id: int) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["messagedata"] = [chat_id, msg_id]
        return self.white(data)

    def set_userdata_status_type(self, user_id: int, status: str) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["type"] = status
        return self.white(data)
    
    def add_userdata_status(self, user_id: int, status: str) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["userdata"].append(status)
        return self.white(data)
    
    def set_userdata_status(self, user_id: int, status: list) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["userdata"] = status
        return self.white(data)

    def set_clear_user_status(self, user_id: int) -> bool:
        data = self.read()
        data[str(user_id)]["status"]["type"] = ""
        data[str(user_id)]["status"]["origin"] = ""
        data[str(user_id)]["status"]["messagedata"] = []
        data[str(user_id)]["status"]["userdata"] = []
        return self.white(data)


    def change_meta_user_by_id(self, user_id: int, datatype: str, new: str):
        data = self.read()
        data[str(user_id)][datatype] = new
        return self.white(data)

    def add_user(self, user_id: int, name: str, age: int, bio: str, wishlist: str, soc_networks: str):
        data = self.read()
        data[str(user_id)]["Name"] = name
        data[str(user_id)]["Age"] = age
        data[str(user_id)]["Bio"] = bio
        data[str(user_id)]["Wishlist"] = wishlist
        data[str(user_id)]["Soc_Nets"] = soc_networks

        return self.white(data)

    def get_user_by_id(self, user_id: int) -> dict:
        return self.read()[str(user_id)]

    def get_data_user_by_id(self, user_id: int) -> dict|None:
        data = self.read()[str(user_id)]
        try: return {
                str(user_id): {
                    "Name": data["Name"],
                    "Age": data["Age"],
                    "Bio": data["Bio"],
                    "Wishlist": data["Wishlist"],
                    "Soc_Nets": data["Soc_Nets"]
                }
            }
        except:
            return None

    def get_username_by_id(self, user_id: int) -> str|None:
        try: return self.read()[str(user_id)]["Name"]
        except: return None
        
    def delete_user(self, user_id: int):
        data = self.read()
        del data[str(user_id)]
        return self.white(data)
    
    def get_user_rooms(self, user_id: int):
        try: return self.read()[str(user_id)]["rooms"]
        except: return None
    
    def add_user_in_room(self, room_id: str, user_id: int):
        data = self.read()
        if not room_id in data[str(user_id)]["rooms"]:
            data[str(user_id)]["rooms"].append(room_id)
            return self.white(data)
        else:
            return False
        

    def delete_user_in_room(self, room_id: str, user_id: int):
        data = self.read()
        data[str(user_id)]["rooms"].remove(room_id)
        return self.white(data)

# r = Users("Data/users.json")
# print(r.add_user(113, "Name", 23, "Ну вот что-то тут пишу", "Хочу что-то"))