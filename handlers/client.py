import logging
from asyncio import get_event_loop, set_event_loop

from aiogram import types, Dispatcher, Bot

from classes.classes_db import InitDB
from classes.templates import Templates
from classes.Keyboard import Keyboard
from classes.functions import Functions


class Client(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        super(Client, self).__init__(bot, db, loop, Keyboards, temp)

        self.log = logging.getLogger('client')

        self.db = db
        self.keyboard = Keyboards
        self.temp = temp

    async def cmdStart(self, message: types.Message):
        self.addUser(f'{message.chat.id}', 0)

        objects = await self.temp.temUser(message.chat.id)
        start_text = self.temp.templates_text(file='start.txt', objects=objects)

        await message.delete()
        await message.answer(start_text)

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(callback=self.cmdStart, commands=['start'], chat_private=True)