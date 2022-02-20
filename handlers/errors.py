import logging
from asyncio import get_event_loop, set_event_loop

from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, TelegramAPIError
from aiogram import types, Dispatcher, Bot

from classes.classes_db import InitDB
from classes.functions import Functions
from classes.Keyboard import Keyboard
from classes.templates import Templates


class Errors(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):

        super(Errors, self).__init__(bot, db, loop, Keyboards, temp)

        self.log = logging.getLogger('errors')

    async def error_BotBlocked(self, update: types.Update, exception: BotBlocked):
        self.addUser(f'{update.message.chat.id}', 1)
        self.log.info(f"{exception}")
        return True

    async def error_ChatNotFound(self, update: types.Update, exception: ChatNotFound):
        self.deleteUser(update.message.chat.id)

        self.log.info(f"{exception}")
        return True

    async def error_UserDeactivated(self, update: types.Update, exception: UserDeactivated):
        self.deleteUser(update.message.chat.id)

        self.log.info(f"{exception}")
        return True

    async def error_TelegramAPIError(self, update: types.Update, exception: TelegramAPIError):
        self.log.info(f"{exception} - TelegramAPIError - {update}")
        return True

    def registerHandlers(self, dp: Dispatcher):
        dp.register_errors_handler(self.error_BotBlocked, exception=BotBlocked)
        dp.register_errors_handler(self.error_ChatNotFound, exception=ChatNotFound)
        dp.register_errors_handler(self.error_UserDeactivated, exception=UserDeactivated)
        dp.register_errors_handler(self.error_TelegramAPIError, exception=TelegramAPIError)