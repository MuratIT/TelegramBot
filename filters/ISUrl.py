import validators
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from classes.gettext import getText


class ISUrl(BoundFilter):
    key = 'is_url'

    def __init__(self, is_url):
        self.is_url = is_url

    async def check(self, message: any):
        if isinstance(message, types.Message):
            if validators.url(message.text, True):
                return True
            else:
                await message.delete()
                await message.answer(getText('url_callback_button_error_validators'))
                return False
        elif isinstance(message, types.CallbackQuery):
            if validators.url(message.message.text, True):
                return True
            else:
                await message.message.delete()
                await message.answer(getText('url_callback_button_error_validators'))
                return False
        return False