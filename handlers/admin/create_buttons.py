from asyncio import get_event_loop, set_event_loop

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from classes.classes_db import InitDB
from classes.templates import Templates
from classes.Keyboard import Keyboard
from classes.functions import Functions
from classes.gettext import getText
from classes.states_group import AdminCreatePost


class CreateButtons(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        super(CreateButtons, self).__init__(bot, db, loop, Keyboards, temp)

        self.db = db
        self.keyboard = Keyboards
        self.temp = temp

        self.button_names = list()
        self.button_url = list()

    async def createButtonsTitle(self, message: types.Message, state: FSMContext):
        if message.text not in self.button_names:
            self.button_names.append(message.text)

            await AdminCreatePost.url.set()
            await message.answer(getText('url_callback_button'))
        else:
            await message.delete()
            await message.answer(getText('title_button_error'))

    async def CreateButtonURL(self, message: types.Message, state: FSMContext):
        if message.text not in self.button_url:
            self.button_url.append(message.text)

            await AdminCreatePost.continues.set()
            keyboard = self.keyboard.loadKeyboard('create_buttons_admin')[0]
            await message.answer(getText('create_button_next'), reply_markup=self.keyboard.inline(keyboard))
        else:
            await message.delete()
            await message.answer('Такая ссылка уже используется! Укажите другую ссылку!')

    async def CreateButtonsContinues(self, CallbackQuery: types.CallbackQuery, state: FSMContext):
        if CallbackQuery.data == 'createButtonYes':
            await AdminCreatePost.title.set()
            await CallbackQuery.message.edit_text(getText('title_button'))

        elif CallbackQuery.data == 'createButtonNo':
            async with state.proxy() as data:
                data['buttons'] = self.keyboard.InlineMenu(self.button_names, self.button_url)

            self.button_names, self.button_url = list(), list()

            await AdminCreatePost.time.set()
            admin_exit = self.keyboard.loadKeyboard('cancellation')[0]
            await CallbackQuery.message.edit_text(getText('time'), reply_markup=self.keyboard.inline(admin_exit))

        await CallbackQuery.answer()

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.createButtonsTitle, content_types='text',
                                    state=AdminCreatePost.title, is_admin=True, chat_private=True)

        dp.register_message_handler(self.CreateButtonURL, content_types='text',
                                    state=AdminCreatePost.url, is_admin=True, chat_private=True, is_url=True)

        dp.register_callback_query_handler(self.CreateButtonsContinues,
                                           Text(equals=self.keyboard.loadKeyboard('create_buttons_admin')[1],
                                                ignore_case=True),
                                           state=AdminCreatePost.continues, is_admin=True, chat_private=True)
