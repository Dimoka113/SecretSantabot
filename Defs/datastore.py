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
    def __init__(self, path): 
        super().__init__(path)
    

    def create_room(self, 
    name: str, 
    admin_data: list,
    peer_limit: int, 
    condition_limit: int,   # Условие обмена
    date_created: datetime, # Время, когда комната была создана
    date_intited: datetime, # Время, когда больше нельзя будет заходить в комнату, и её настраивать
    date_roll: datetime,    # Время, когда запуститься жеребьёвка
    date_limit: datetime    # Время, сколько будет существовать комната
                    ):
        data = self.read()
        data[get_random_id()] = {
        "name": name,
        "admin": admin_data,
        "condition_limit": condition_limit,
        "peer_limit": peer_limit,
        "date_created": date_created,
        "date_intited": date_intited,
        "date_roll": date_roll,
        "date_limit": date_limit,
        }
        return self.white(data)
        # ...

    def add_user_in_room(self, room_id: str, user_id: int) -> bool:
        data = self.read()
        data[room_id]["users"].append(user_id)
        return self.white(data)

    def get_roomname_by_id(self, room_id: str) -> str:
        return self.read()[room_id]["name"]
    
    def get_admins_by_id(self, room_id: str) -> str:
        return self.read()[room_id]["admin"]

    def get_rooms(self):
        return [i for i in self.read()]

    def delete_room(self, room_id: str) -> bool:
        data = self.read()
        del data[room_id]
        return self.white(data)
    
    def get_users_room_by_user_id(user_id: int):
        # ...
        return []

class Users(Gateway):
    def __init__(self, path): 
        super().__init__(path)


    def add_user(self, user_id: int, name: str, age: int, wishlist: str, bio: str, soc_networks: str):
        data = self.read()
        data[str(user_id)] = {
            "create": "",
            "Name": name, 
            "Age": age, 
            "Bio": bio, 
            "Soc_Nets": soc_networks,
            "Wishlist": wishlist, 
        }
        return self.white(data)

    def get_user_by_id(self, id: int) -> str:
        return self.read()[id]

    def get_username_by_id(self, id: int) -> str:
        return self.read()[id]["Name"]
    
    def delete_user(self, id: int):
        data = self.read()
        del data[str(id)]
        return self.white(data)
    
    def add_user_in_room(self, room_id: int, user_id: int):
        data = self.read()
        data[str(user_id)]["rooms"].append(room_id)
        return self.white(data)

# r = Users("Data/users.json")
# print(r.add_user(113, "Name", 23, "Ну вот что-то тут пишу", "Хочу что-то"))