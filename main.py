from pyrogram import types, idle
from Bot.loader import bot, log, lang
import json, asyncio
import logging
logging.basicConfig(level=logging.INFO)
import Handlers

# async def test():
#     await bot.start()

#     await idle()


if __name__ == "__main__":
    log.info(lang._text("_log_staring_message"))
    # bot.run(test())
    bot.run()
