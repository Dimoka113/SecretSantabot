import json
from Defs.random_id import get_random_id
from datetime import datetime


class Gateway(object):
    path = str()
    def __init__(self, path: str):
        self.path = path

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
    admin_data: list,
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
        "peer_limit": int(peer_limit),
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

    def delete_user_in_room(self, room_id: str, user_id: int|str) -> bool:
        data = self.read()
        del data[room_id]["users"][str(user_id)]
        return self.white(data)

    def get_roomname_by_id(self, room_id: str) -> str:
        return self.read()[room_id]["name"]
    
    def get_admins_by_id(self, room_id: str) -> int:
        return int(self.read()[room_id]["admin"][0])

    def get_rooms(self):
        return [i for i in self.read()]

    def delete_room(self, room_id: str) -> bool:
        data = self.read()
        del data[room_id]
        return self.white(data)
    
    def get_users_room_by_room_id(self, room_id: str):
        data = self.read()
        return [int(i) for i in data[room_id]["users"]]

class Users(Gateway):
    def __init__(self, path): 
        super().__init__(path)

    def add_zero_user(self, user_id: int):
        data = self.read()
        data[str(user_id)] = {"status": {"type": "", "origin": "", "messagedata": [], "userdata": []}}
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
    
    def get_messagedata_type(self, user_id: int) -> str:
        data = self.read()
        return data[str(user_id)]["status"]["type"]
    
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

    def get_data_user_by_id(self, user_id: int) -> dict:
        data = self.read()[str(user_id)]
        return {
            str(user_id): {
                "Name": data["Name"],
                "Age": data["Age"],
                "Bio": data["Bio"],
                "Wishlist": data["Wishlist"],
                "Soc_Nets": data["Soc_Nets"]
            }
        }
    

    def get_username_by_id(self, user_id: int) -> str:
        return self.read()[str(user_id)]["Name"]
    
    def delete_user(self, user_id: int):
        data = self.read()
        del data[str(user_id)]
        return self.white(data)
    
    def add_user_in_room(self, room_id: int, user_id: int):
        data = self.read()
        data[str(user_id)]["rooms"].append(room_id)
        return self.white(data)

# r = Users("Data/users.json")
# print(r.add_user(113, "Name", 23, "Ну вот что-то тут пишу", "Хочу что-то"))