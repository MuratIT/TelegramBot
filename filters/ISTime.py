from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from classes.gettext import getText


class ISTime(BoundFilter):
    key = 'is_time'

    def __init__(self, is_time):
        self.is_time = is_time

    async def check(self, message: any):
        if isinstance(message, types.Message):
            try:
                datetime.strptime(message.text, '%d.%m.%Y %H:%M:%S')
                return True
            except ValueError:
                await message.delete()
                await message.answer(getText('time_error_validators'))
                return False
        elif isinstance(message, types.CallbackQuery):
            try:
                datetime.strptime(message.message.text, '%d.%m.%Y %H:%M:%S')
                return True
            except ValueError:
                await message.message.delete()
                message_text = message.message.text
                await message.answer(getText('time_error_validators'))
                return False
        return False