import asyncio

from aiogram import executor

from db import db_init
from handlers import dp
from parser import Parser


async def on_startup(dp):
    await db_init()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    parser = Parser(loop)
    parser.start()

    executor.start_polling(dp, on_startup=on_startup, loop=loop)