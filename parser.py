import asyncio

from loader import bot
from models import TelegramUser
import requests
from bs4 import BeautifulSoup as bs4


class Parser(object):
    loop = None
    instance = None
    pool = None

    def __new__(cls, loop):
        if not cls.instance:
            cls.instance = super(Parser, cls).__new__(cls)
            cls.pool = {}
            cls.loop = loop

        return cls.instance

    async def parse_user(self, user: TelegramUser):
        resp = requests.get(f'https://kwork.ru/projects?keyword={await user.format_words}&c=all')
        soup = bs4(resp.content, 'html.parser')
        pool = []
        for element in soup.find_all('div', class_='wants-card__header-title'):
            url = element.find('a')['href']
            pool.append(url)
            if self.pool.get(user.id):
                if url not in self.pool[user.id]:
                    await bot.send_message(
                        user.telegram_id,
                        url
                    )
            else:
                self.pool[user.id] = []

        self.pool[user.id] = pool

    async def parse_users(self):
        users = await TelegramUser.filter(active=True)
        for user in users:
            await self.parse_user(user)

    async def cycle(self):
        while True:
            await self.parse_users()
            await asyncio.sleep(300)

    def start(self):
        self.loop.create_task(self.cycle())





