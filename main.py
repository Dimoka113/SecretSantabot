from pyrogram import types, idle, Client

# Set the logging level before creating the logger class.
# (Otherwise, it will always be Logger.types.INFO)
from Defs.logger import Logger
Logger.level(Logger.types.DEBUG)

import Handlers
from Bot.loader import bot, log, lang, databot
from utils.set_bot_commands import set_default_commands

import logging
logging.basicConfig(level=logging.INFO)


async def thread():
    await bot.start()
    await databot.update_bot(bot)
    log.info(lang._text("_log_staring_message"))
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
    try:
        bot.run(thread())
    except:
        log.crit(lang._text("_log_error_staring_message"))