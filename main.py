from pyrogram import types, idle
from Bot.loader import bot, log, lang
import json, asyncio
import logging
from Defs.logger import Logger
import Handlers
from utils.set_bot_commands import set_default_commands

log.level(Logger.types.DEBUG)
logging.basicConfig(level=logging.INFO)


async def thread():
    await bot.start()
    await set_default_commands(bot)
    await idle()


if __name__ == "__main__":
    log.info(lang._text("_log_staring_message"))
    bot.run(thread())
