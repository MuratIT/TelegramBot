from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    def __init__(self):
        self.remove = ReplyKeyboardRemove()

    @staticmethod
    def __listInlineKeyboardButton(lists: list):
        buttons = list()

        for item in lists:
            callback_data = None if item['callback_data'] is False or item['callback_data'] is None \
                else item['callback_data']

            url = None if item['url'] is False or item['url'] is None else item['url']

            inline_btn = InlineKeyboardButton(item['title'], callback_data=callback_data, url=url)
            buttons.append(inline_btn)

        return buttons

    @staticmethod
    def __listsReplyButtons(lists: list):
        arr = list()
        for item in lists:
            if type(item) == str:
                arr.append(KeyboardButton(item))
        return arr

    def inline(self, lists: list):
        inline_kb = InlineKeyboardMarkup()
        for item in lists:
            if type(item) == dict:
                callback_data = None if item['callback_data'] is False or item['callback_data'] is None \
                    else item['callback_data']

                url = None if item['url'] is False or item['url'] is None else item['url']

                inline_btn = InlineKeyboardButton(item['title'], callback_data=callback_data, url=url)
                inline_kb.add(inline_btn)
            elif type(item) == list:
                s = self.__listInlineKeyboardButton(item)
                inline_kb.row(*s)
        return inline_kb

    def reply(self, lists: list):
        reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in lists:
            if type(item) == str:
                reply_keyboard_markup.add(KeyboardButton(item))
            elif type(item) == list:
                arr = self.__listsReplyButtons(item)
                reply_keyboard_markup.row(*arr)
        return reply_keyboard_markup