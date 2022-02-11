import os

import validators
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from classes.gettext import getText
from classes.classes_db import InitDB
from classes.Keyboard import Keyboard
from classes.templates import Templates
from classes.states_group import AdminCreatePost


class CreateButtons:
    def __init__(self, db: InitDB, keyboard: Keyboard, temp: Templates):
        self.db = db
        self.keyboard = keyboard
        self.temp = temp
        self.admin_username = os.environ.get('ADMIN_USERNAME')

        self.button_menu_names = ['Да', 'Нет']
        self.button_menu_object = self.keyboard.InlineMenu(self.button_menu_names)
        self.button_menu = self.keyboard.inline(self.button_menu_object)

        self.buttons_names = list()
        self.buttons_url = list()

    async def CreateButtonTitle(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:

            if message.text not in self.buttons_names:
                self.buttons_names.append(message.text)

                await AdminCreatePost.url.set()
                await message.answer(getText('url_callback_button'))
            else:
                await message.delete()
                await message.answer(getText('title_button_error'))

    async def CreateButtonURL(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:

            if message.text not in self.buttons_url:
                if validators.url(message.text, True):
                    self.buttons_url.append(message.text)

                    await AdminCreatePost.continues.set()
                    await message.answer(getText('create_button_next'), reply_markup=self.button_menu)
                else:
                    await message.delete()
                    await message.answer(getText('url_callback_button_error_validators'))
            else:
                await message.delete()
                await message.answer(getText('url_callback_button_error_repeated'))

    async def CreateButtonsContinues(self, CallbackQuery: types.CallbackQuery, state: FSMContext):
        if CallbackQuery.message.chat.type == 'private' \
                and CallbackQuery.message.chat.username == self.admin_username:

            if CallbackQuery.data == self.button_menu_names[0]:
                await AdminCreatePost.title.set()
                await CallbackQuery.message.edit_text(getText('title_button'))

            elif CallbackQuery.data == self.button_menu_names[1]:
                async with state.proxy() as data:
                    data['buttons'] = self.keyboard.InlineMenu(self.buttons_names, self.buttons_url)

                self.buttons_names, self.buttons_url = list(), list()

                await AdminCreatePost.time.set()
                await CallbackQuery.message.edit_text(getText('time'),
                                                      reply_markup=self.keyboard.inlineAddCallback(['Отмена']))

        await CallbackQuery.answer()

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.CreateButtonTitle, content_types='text', state=AdminCreatePost.title)
        dp.register_message_handler(self.CreateButtonURL, content_types='text', state=AdminCreatePost.url)

        dp.register_callback_query_handler(self.CreateButtonsContinues,
                                           Text(equals=self.button_menu_names, ignore_case=True),
                                           state=AdminCreatePost.continues)