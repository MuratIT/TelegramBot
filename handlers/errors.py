from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, TelegramAPIError
from aiogram import types, Dispatcher
from classes.db import DB
import logging


class Errors:
    def __init__(self, db: DB):
        self.log = logging.getLogger('errors')
        self.db = db

    def addUser(self, id_user: str, active: str, passive: str):
        insert = self.db.insertUsers(id_user, active)
        if not insert:
            if self.db.selectUsers(id_user)['blocked'] == passive:
                self.db.updateUsersBlocked(id_user, active)

    async def error_BotBlocked(self, update: types.Update, exception: BotBlocked):
        self.addUser(f'{update.message.chat.id}', '1', '0')
        self.log.info(f"{exception}")
        return True

    async def error_ChatNotFound(self, update: types.Update, exception: ChatNotFound):
        self.db.deleteUser(f"{update.message.chat.id}")
        self.log.info(f"{exception}")
        return True

    async def error_UserDeactivated(self, update: types.Update, exception: UserDeactivated):
        self.db.deleteUser(f"{update.message.chat.id}")
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