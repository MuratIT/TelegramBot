import os
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
from jinja2 import Environment, FileSystemLoader

from classes.classes_db import InitDB
from classes.Keyboard import Keyboard
from classes.templates import Templates
from classes.Broadcaster import Broadcaster
from handlers.errors import Errors
from handlers.client import Client
from handlers.admin.create_buttons import CreateButtons
from handlers.admin.create_post import CreatePost
from handlers.admin.admin import Admin


strfmt = '[%(asctime)s] | [%(name)s] | [%(levelname)s] | %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, format=strfmt, datefmt=datefmt, filename='logging.log')


class TelegramBot:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

        self.db = InitDB()
        self.db.createDatabase()

        self.keyboard = Keyboard()

        self.env = Environment(loader=FileSystemLoader('text_templates'), trim_blocks=True)

        self.bot = Bot(os.environ.get('TOKEN'), parse_mode='HTML')
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

        self.temp = Templates(self.bot, self.env)

    async def on_startup(self, dp: Dispatcher):
        error = Errors(self.db)
        client = Client(self.db, self.keyboard, self.temp, error)

        create_buttons = CreateButtons(self.db, self.keyboard, self.temp)
        create_post = CreatePost(self.db, self.keyboard, self.temp)
        admin = Admin(self.db, self.bot, self.keyboard, self.temp)

        await Broadcaster(self.bot, self.db, self.loop, self.keyboard, self.temp).run()

        error.registerHandlers(dp)
        client.registerHandlers(dp)

        create_buttons.registerHandlers(dp)
        create_post.registerHandlers(dp)
        admin.registerHandlers(dp)

    def run(self):
        executor.start_polling(self.dp, loop=self.loop, skip_updates=True, on_startup=self.on_startup)


if __name__ == "__main__":
    telegram_bot = TelegramBot()
    telegram_bot.run()