import os
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
from jinja2 import Environment, FileSystemLoader

from classes.load import loadClasses
from classes.classes_db import InitDB
from classes.Keyboard import Keyboard
from classes.templates import Templates
from classes.Broadcaster import Broadcaster
from handlers.errors import Errors
from handlers.client import Client
from handlers.admin.admin import Admin
from handlers.admin.create_post import CreatePost
from handlers.admin.create_buttons import CreateButtons


strfmt = '[%(asctime)s] | [%(name)s] | [%(levelname)s] | %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, format=strfmt, datefmt=datefmt)


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

    @staticmethod
    async def Loads_filters(dp: Dispatcher):
        for class_ in loadClasses('filters'):
            dp.filters_factory.bind(class_)

    async def Loads_modules(self, dp: Dispatcher):
        for class_ in loadClasses('modules'):
            classes = class_(self.bot, self.db, self.loop, self.keyboard, self.temp)

            if 'run' in dir(classes):
                classes.run()
            elif 'runAsync' in dir(classes):
                await classes.runAsync()

            if 'registerHandlers' in dir(classes):
                classes.registerHandlers(dp)

    async def on_startup(self, dp: Dispatcher):
        error = Errors(self.bot, self.db, self.loop, self.keyboard, self.temp)
        client = Client(self.bot, self.db, self.loop, self.keyboard, self.temp)
        admin = Admin(self.bot, self.db, self.loop, self.keyboard, self.temp)
        create_post = CreatePost(self.bot, self.db, self.loop, self.keyboard, self.temp)
        create_buttons = CreateButtons(self.bot, self.db, self.loop, self.keyboard, self.temp)

        await Broadcaster(self.bot, self.db, self.loop, self.keyboard, self.temp).run()

        await self.Loads_filters(dp)

        error.registerHandlers(dp)
        client.registerHandlers(dp)
        admin.registerHandlers(dp)
        create_post.registerHandlers(dp)
        create_buttons.registerHandlers(dp)

        await self.Loads_modules(dp)

    def run(self):
        executor.start_polling(self.dp, loop=self.loop, skip_updates=True, on_startup=self.on_startup)


if __name__ == "__main__":
    telegram_bot = TelegramBot()
    telegram_bot.run()