from handlers.adminHandlers.create_posts import CreatePost
from aiogram.dispatcher.filters import Text
from classes.templates import Templates
from classes.Keyboard import Keyboard
from aiogram import Dispatcher, types
from classes.db import DB
import logging


class Admin(CreatePost):
    def __init__(self, db: DB, admin_chat_id: str, temp: Templates, keyboards: Keyboard):
        super(Admin, self).__init__(db, admin_chat_id, keyboards)

        self.db = db
        self.admin_chat_id = admin_chat_id
        self.temp = temp
        self.keyboards = keyboards
        self.log = logging.getLogger('Admin')

        self.admin_menu = [
            [
                {'title': 'Статистика', 'callback_data': 'statistics', 'url': False},
                {'title': 'Рассылка', 'callback_data': 'mailing', 'url': False},
            ]
        ]

        self.admin_menu_exit = [
            {'title': 'Назад', 'callback_data': 'admin_exit', 'url': False}
        ]

        self.admin_menu_mailing = [
            [
                {'title': 'Создать пост', 'callback_data': 'create_post', 'url': False},
                {'title': 'Создать кнопку', 'callback_data': 'create_button', 'url': False},
            ],
            *self.admin_menu_exit
        ]

    async def __adminText(self, message: types.Message):
        objects = await self.temp.temUser(message.chat.id)
        return self.temp.templates_text('admin.txt', objects)

    async def cmdAdmin(self, message: types.Message):
        if self.chAdmin(message):
            text_admin = await self.__adminText(message)
            await message.answer(text_admin, reply_markup=self.keyboards.inline(self.admin_menu))

    async def callbackDataStatistics(self, callback_query: types.CallbackQuery):
        if self.chAdmin(callback_query.message):
            objects = {
                'active_users': self.db.selectUsersCount('0')['count'],
                'passive_users': self.db.selectUsersCount('1')['count']
            }
            text_statistics = self.temp.templates_text('statistics.txt', objects)

            await callback_query.message.edit_text(text_statistics,
                                                   reply_markup=self.keyboards.inline(self.admin_menu_exit))

        await callback_query.answer()

    async def callbackDataMailing(self, callback_query: types.CallbackQuery):
        if self.chAdmin(callback_query.message):
            text_mailing = self.temp.templates_text('mailing.txt')
            await callback_query.message.edit_text(text_mailing,
                                                   reply_markup=self.keyboards.inline(self.admin_menu_mailing))
        await callback_query.answer()

    async def callbackDataExit(self, callback_query: types.CallbackQuery):
        if self.chAdmin(callback_query.message):
            text_admin = await self.__adminText(callback_query.message)
            await callback_query.message.edit_text(text_admin, reply_markup=self.keyboards.inline(self.admin_menu))
        await callback_query.answer()

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.cmdAdmin, commands=['admin'])

        dp.register_callback_query_handler(self.callbackDataStatistics, Text(equals='statistics', ignore_case=True))

        dp.register_callback_query_handler(self.callbackDataMailing, Text(equals='mailing', ignore_case=True))

        self.registerHandlersCreatePost(dp)

        dp.register_callback_query_handler(self.callbackDataExit, Text(equals='admin_exit', ignore_case=True))