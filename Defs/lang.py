from Defs.datastore import Gateway
import random

class Lang(Gateway):
    """
    Class for selecting the bot's language.
    The default is "en".
    
    """

    def __init__(self, path: str, lang: str = "en", logger = None):
        filepath = path + "/" + lang + ".json"
        super().__init__(filepath, logger)

    def _text(self, *path: str) -> str:
        data = self.read()
        for key in path: data = data[key]

        if isinstance(data, list): return data[random.randint(0, len(data)-1)]
        elif isinstance(data, str): return data

    def get_command(self) -> dict:
        return self.read()["commands"]