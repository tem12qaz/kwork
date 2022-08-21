import asyncio

from aiogram import executor

from db import db_init
from handlers import dp
from parser import Parser


async def on_startup(dp):
    await db_init()
    loop = asyncio.get_running_loop()
    parser = Parser(loop)
    parser.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)