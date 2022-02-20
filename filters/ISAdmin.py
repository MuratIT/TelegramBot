import os

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ISAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: any):
        if isinstance(message, types.Message):
            if os.environ.get('ADMIN_USERNAME') == message.from_user.username:
                return True
            return False
        elif isinstance(message, types.CallbackQuery):
            if os.environ.get('ADMIN_USERNAME') == message.message.chat.username:
                return True
            return False
        return False