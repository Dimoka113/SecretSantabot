from Bot.loader import bot, lang
from Data import config
from pyrogram import Client, types, filters


@bot.on_message(filters.command(commands="start", prefixes=["/", "!"]))
async def start_command(origin: Client, msg: types.Message):
    if len(msg.text.split()) == 1:
        await msg.reply(lang._text("start_message"))
    else:
        await msg.reply(lang._text("join_message"))
