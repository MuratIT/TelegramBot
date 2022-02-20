import json

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from classes.classes_db import InitDB
from classes.classes_db import KeyboardDB


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
    def __loadKeyboards():
        with open('keyboard.json', encoding='utf-8') as f:
            read = json.load(f)
        return read

    @staticmethod
    def InlineMenu(names: list = None, urls: list = None, callback_data: list = None):
        objects = list()
        if names and not urls:
            for key, name in enumerate(names):
                if callback_data:
                    if len(callback_data) == len(names):
                        objects.append({'title': name, 'callback_data': callback_data[key], 'url': None})
                else:
                    objects.append({'title': name, 'callback_data': name, 'url': None})

        if urls:
            for key, name in enumerate(names):
                objects.append({'title': name, 'callback_data': None, 'url': urls[key]})

        return objects

    @staticmethod
    def loadDynamicKeyboard(db: InitDB, name: str):
        with db.session_scope() as session:
            keyboard = session.query(KeyboardDB).filter(KeyboardDB.name == name).first()
            if keyboard:
                return json.loads(keyboard.reply_markup)
            return None

    def loadDynamicKeyboardCallbackDataList(self, db: InitDB, name: str):
        keyboard = self.loadDynamicKeyboard(db, name)
        if keyboard:
            callback_data = set()
            for item in keyboard:
                items = item['callback_data']
                if items:
                    callback_data.add(items)
            return tuple(callback_data)
        return None

    def createInlineDynamicKeyboard(self, db: InitDB, name: str, title_call: list, urls: list = None,
                                    callback_data: list = None):
        select = self.loadDynamicKeyboard(db, name)
        if not select:
            inline_menu = self.InlineMenu(title_call, urls, callback_data)
            with db.session_scope() as session:
                if not self.loadDynamicKeyboard(db, name):
                    keyboard = KeyboardDB(name, json.dumps(inline_menu, ensure_ascii=False))
                    session.add(keyboard)
                    session.commit()
            return True
        return False

    def updateDynamicKeyboard(self, db: InitDB, name: str, title_call: list,
                              urls: list = None, save: bool = False, callback_data: list = None):
        select = self.loadDynamicKeyboard(db, name)
        if select:
            with db.session_scope() as session:
                inline_menu = self.InlineMenu(title_call, urls, callback_data)
                if save:
                    array = list()
                    for i in select:
                        array.append(i)
                    for i in inline_menu:
                        if i not in select:
                            array.append(i)

                    session.query(KeyboardDB).filter(KeyboardDB.name == name).update(
                        {'reply_markup': json.dumps(array, ensure_ascii=False)})
                else:
                    session.query(KeyboardDB).filter(KeyboardDB.name == name).update(
                        {'reply_markup': json.dumps(inline_menu, ensure_ascii=False)})

                session.commit()
                return True
        return False

    def loadKeyboard(self, name: str):
        try:
            item = self.__loadKeyboards()[name]
            callback_data = set()
            for i in item:
                if i['callback_data']:
                    callback_data.add(i['callback_data'])
            return item, tuple(callback_data)
        except Exception:
            return None, None

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