from Defs.datastore import Gateway


class Lang(Gateway):
    """
    Class for selecting the bot's language.
    The default is "en".
    
    """
    def __init__(self, path: str, lang: str = "en"):
        filepath = path + "/" + lang + "json"
        super().__init__(filepath)

    def _text(self, data: str) -> str:
        return self.read()[data]