from pyrogram import types, idle
from Bot.loader import bot, log, lang
import json, asyncio
import logging
logging.basicConfig(level=logging.INFO)
import Handlers
from utils.set_bot_commands import set_default_commands


async def thread():
    await bot.start()
    await set_default_commands(bot)
    await idle()


if __name__ == "__main__":
    log.info(lang._text("_log_staring_message"))
    bot.run(thread())
    bot.run()
