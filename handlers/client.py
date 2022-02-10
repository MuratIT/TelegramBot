import logging

from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from classes.classes_db import InitDB
from classes.templates import Templates
from classes.Keyboard import Keyboard
from handlers.errors import Errors


class Client:
    def __init__(self, db: InitDB, keyboards: Keyboard, temp: Templates, error: Errors):
        self.log = logging.getLogger('client')

        self.db = db
        self.keyboard = keyboards
        self.temp = temp
        self.__addUser = error.addUser

    async def cmdStart(self, message: types.Message):
        if message.chat.type == 'private':
            self.__addUser(f'{message.chat.id}', 0)

            objects = await self.temp.temUser(message.chat.id)
            start_text = self.temp.templates_text(file='start.txt', objects=objects)

            await message.delete()
            await message.answer(start_text)

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(callback=self.cmdStart, commands=['start'])