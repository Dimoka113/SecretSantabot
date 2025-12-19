from pyrogram import types, idle
from Bot.loader import bot, log, lang, databot
import json, asyncio
import logging
from Defs.logger import Logger
import Handlers
from utils.set_bot_commands import set_default_commands

log.level(Logger.types.DEBUG)
logging.basicConfig(level=logging.INFO)


async def thread():
    await bot.start()
    await databot.update_bot(bot)
    log.info(
        lang._text("_log_data_bot_done")
        .format(
            botname=databot.first_name,
            botusername=databot.username
        )
    )
    await set_default_commands(bot)
    await idle()

if __name__ == "__main__":
    log.info(lang._text("_log_staring_message"))
    bot.run(thread())
