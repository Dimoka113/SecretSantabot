from pyrogram import types


def create_keybord(keys: list[list[str]]) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(text=label[0], callback_data=label[1]) for label in row
            ]
            for row in keys
        ]
    )

def create_keybord_links(keys: list[list[str]]) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(text=label[0], url=label[1]) for label in row
            ]
            for row in keys
        ]
    )
