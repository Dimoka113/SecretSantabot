from pyrogram import types, Client
from Bot.loader import lang, log


async def set_default_commands(dp: Client) -> bool:
    data = []
    commands = lang.get_command()
    for command in commands:
       data.append(types.BotCommand(command, commands[command]))


    bot_command = await dp.get_bot_commands()
    if data != bot_command:
        log.warn(data)
        return await dp.set_bot_commands(data)
    else:
        return False