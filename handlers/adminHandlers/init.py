from aiogram import types


class InitAdmin:
    def __init__(self, admin_chat_id: str):
        self.admin_chat_id = admin_chat_id

    def chAdmin(self, message: types.Message):
        if message.chat.type == 'private' and str(message.chat.id) == str(self.admin_chat_id):
            return True
        return False