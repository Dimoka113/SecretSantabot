import json
from Defs.random_id import get_random_id
from datetime import datetime
# from Bot.loader import log


class Gateway(object):
    path = str()
    def __init__(self, path: str):
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r", encoding="UTF-8") as file: 
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as err:
                # log.warn(err);
                return {}

    def white(self, data: dict) -> bool:
        """
Returns `True` if successful.

If unsuccessful, outputs a log with `WARN` and returns `False`.
        """
        try: 
            with open(self.path, "w", encoding="UTF-8") as file: json.dump(data, file, indent=3, ensure_ascii=False)
        except Exception as err:
            # log.warn(err)
            return False
        else: return True


class Rooms(Gateway):
    def __init__(self, path): 
        super().__init__(path)
    
    def create_room(self, 
    name: str, 
    admin_id: int,
    peer_limit: int, 
    money_limit: int, # Бюджет? (Заменить на?) ( https://t.me/c/3361797240/11 )
    date_created: datetime, # Время, когда комната была создана
    date_intited: datetime, # Время, когда больше нельзя будет заходить в комнату, и её настраивать
    date_roll: datetime,    # Время, когда запуститься жеребьёвка
    date_limit: datetime    # Время, сколько будет существовать комната
                    ):
        data = self.read()
        data[get_random_id()] 



class Users(Gateway):
    def __init__(self, path): 
        super().__init__(path)


    def add_user(self, user_id: int, name: str, age: int, wishlist: str, bio: str, soc_networks: str):
        data = self.read()
        data[str(user_id)] = {
            "Name": name, 
            "Age": age, 
            "Bio": bio, 
            "Soc_Nets": soc_networks,
            "Wishlist": wishlist, 
            "rooms": []}
        return self.white(data)

    def get_user_by_id(self, id: int) -> str:
        return self.read()[id]

    def get_username_by_id(self, id: int) -> str:
        return self.read()[id]["Name"]
    
    def delete_user(self, id: int):
        data = self.read()
        del data[str(id)]
        return self.white(data)
    
    def add_user_in_room(self, user_id: int, room_id: int):
        data = self.read()
        data[str(user_id)]["rooms"].append(room_id)


# r = Users("Data/users.json")
# print(r.add_user(113, "Name", 23, "Ну вот что-то тут пишу", "Хочу что-то"))