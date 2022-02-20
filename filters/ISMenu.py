from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ISMenu(BoundFilter):
    key = 'is_menu'

    def __init__(self, is_menu):
        self.is_menu = is_menu

    async def check(self, message: any):
        db = self.is_menu[0]
        keyboard = self.is_menu[1]
        name = self.is_menu[2]
        if isinstance(message, types.CallbackQuery):
            text = message.data
            if text in keyboard.loadDynamicKeyboardCallbackDataList(db, name):
                return True
        return False