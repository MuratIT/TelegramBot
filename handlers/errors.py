import logging

from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated, TelegramAPIError
from aiogram import types, Dispatcher

from classes.classes_db import InitDB
from classes.classes_db import UsersDB


class Errors:
    def __init__(self, db: InitDB):
        self.log = logging.getLogger('errors')
        self.db = db

    def _deleteUser(self, id_chat: str):
        with self.db.session_scope() as session:
            session.query(UsersDB).filter(UsersDB.id_chat == id_chat).delete()

    def addUser(self, id_chat: str, blocked: int):
        with self.db.session_scope() as session:
            select = session.query(UsersDB).filter(UsersDB.id_chat == id_chat).first()
            if not select:
                user = UsersDB(id_chat, blocked)
                session.add(user)
            else:
                session.query(UsersDB).filter(UsersDB.id_chat == select.id_chat).update({'blocked': blocked})
            session.commit()

    async def error_BotBlocked(self, update: types.Update, exception: BotBlocked):
        self.addUser(f'{update.message.chat.id}', 1)
        self.log.info(f"{exception}")
        return True

    async def error_ChatNotFound(self, update: types.Update, exception: ChatNotFound):
        self._deleteUser(update.message.chat.id)

        self.log.info(f"{exception}")
        return True

    async def error_UserDeactivated(self, update: types.Update, exception: UserDeactivated):
        self._deleteUser(update.message.chat.id)

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