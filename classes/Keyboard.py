from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    def __init__(self):
        self.remove = ReplyKeyboardRemove()

    @staticmethod
    def __edit_item_list(lists: list, counts: int):
        buttons = list()
        for i in range(0, len(lists), counts):
            buttons.append(lists[i:i + counts])
        return buttons

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

    @staticmethod
    def InlineMenu(names: list = None, urls: list = None):
        objects = list()
        if names and not urls:
            for name in names:
                objects.append({'title': name, 'callback_data': name, 'url': None})

        if urls:
            for key, name in enumerate(names):
                objects.append({'title': name, 'callback_data': None, 'url': urls[key]})

        return objects

    def inline(self, lists: list, count: int = 1):
        lists = self.__edit_item_list(lists, count)

        inline_kb = InlineKeyboardMarkup()
        for item in lists:
            if type(item) == dict:
                callback_data = None if item['callback_data'] is False or item['callback_data'] is None \
                    else item['callback_data']

                url = None if item['url'] is False or item['url'] is None else item['url']

                inline_btn = InlineKeyboardButton(item['title'], callback_data=callback_data, url=url)
                inline_kb.add(inline_btn)
            elif type(item) == list:
                list_inline_keyboard_button = self.__listInlineKeyboardButton(item)
                inline_kb.row(*list_inline_keyboard_button)
        return inline_kb

    def inlineAddCallback(self, names: list = None, count: int = 1):
        buttons_object = self.InlineMenu(names)
        return self.inline(buttons_object, count)

    def reply(self, lists: list, count: int = 0):
        lists = self.__edit_item_list(lists, count)

        reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in lists:
            if type(item) == str:
                reply_keyboard_markup.add(KeyboardButton(item))
            elif type(item) == list:
                arr = self.__listsReplyButtons(item)
                reply_keyboard_markup.row(*arr)
        return reply_keyboard_markup