import logging

from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, TelegramAPIError
from aiogram import types, Dispatcher

from classes.classes_db import InitDB
from classes.classes_db import UsersDB


class Errors:
    def __init__(self, db: InitDB):
        self.log = logging.getLogger('errors')
        self.db = db

    def addUser(self, id_chat: str, blocked: int):
        @self.db.sessionDB(UsersDB)
        def wrapper(object_db, query, session_db):
            select = query.filter(object_db.id_chat == id_chat).first()
            if not select:
                users = object_db(id_chat, blocked)
                session_db.add(users)
                session_db.commit()
            else:
                query.filter(object_db.id_chat == select.id_chat).update({'blocked': blocked})
                session_db.commit()

    async def error_BotBlocked(self, update: types.Update, exception: BotBlocked):
        self.addUser(f'{update.message.chat.id}', 1)
        self.log.info(f"{exception}")
        return True

    async def error_ChatNotFound(self, update: types.Update, exception: ChatNotFound):
        @self.db.sessionDB(UsersDB)
        def deleteUser(object_db, query, session_db):
            query.filter(object_db.id_chat == update.message.chat.id).delete()

        self.log.info(f"{exception}")
        return True

    async def error_UserDeactivated(self, update: types.Update, exception: UserDeactivated):
        @self.db.sessionDB(UsersDB)
        def deleteUser(object_db, query, session_db):
            query.filter(object_db.id_chat == update.message.chat.id).delete()

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