from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ISPrivateChat(BoundFilter):
    key = 'chat_private'

    def __init__(self, chat_private):
        self.chat_private = chat_private

    async def check(self, message: any):
        if isinstance(message, types.Message):
            if message.chat.type == 'private':
                return True
            return False
        elif isinstance(message, types.CallbackQuery):
            if message.message.chat.type == 'private':
                return True
            return False
        return False