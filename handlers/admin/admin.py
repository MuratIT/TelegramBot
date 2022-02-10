import os

from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from classes.classes_db import InitDB
from classes.classes_db import UsersDB
from classes.Keyboard import Keyboard
from classes.templates import Templates
from classes.states_group import AdminCreatePost


class Admin:
    def __init__(self, db: InitDB, bot: Bot, keyboards: Keyboard, temp: Templates):
        self.db = db
        self.bot = bot
        self.keyboards = keyboards
        self.temp = temp
        self.admin_username = os.environ.get('ADMIN_USERNAME')

        self.names_admin_menu = ['Статистика', 'Создать пост', 'logging file']
        self.admin_menu_object = self.keyboards.InlineMenu(self.names_admin_menu)
        self.admin_menu_inline = self.keyboards.inline(self.admin_menu_object, 2)

        self.nameExit_admin_menu = ['Ввернутся назад']
        self.admin_menu_exit_object = self.keyboards.InlineMenu(self.nameExit_admin_menu)
        self.admin_menu_exit = self.keyboards.inline(self.admin_menu_exit_object)

        self.logger_message_id = None

    def __statistics(self, objects: dict):
        with self.db.session_scope() as session:
            objects['all_users'] = session.query(UsersDB).count()
            objects['active_users'] = session.query(UsersDB).filter(UsersDB.blocked == 0).count()
            objects['passive_users'] = session.query(UsersDB).filter(UsersDB.blocked == 1).count()

        return objects

    async def __templateText_cmdAdmin(self, id_user: str):
        objects = await self.temp.temUser(id_user)
        return self.temp.templates_text('admin.txt', objects)

    async def cmdAdmin(self, message: types.Message):
        if message.chat.type == 'private' and message.chat.username == self.admin_username:
            text_admin = await self.__templateText_cmdAdmin(message.chat.id)
            await message.delete()
            await message.answer(text_admin, reply_markup=self.admin_menu_inline)

    async def cmdAdminMenu(self, callback_query: types.CallbackQuery):
        if callback_query.message.chat.type == 'private' \
                and callback_query.message.chat.username == self.admin_username:

            if callback_query.data == self.names_admin_menu[0]:
                objects = dict()
                objects = self.__statistics(objects)
                text_statistics = self.temp.templates_text('statistics.txt', objects)
                await callback_query.message.edit_text(text_statistics, reply_markup=self.admin_menu_exit)

            elif callback_query.data == self.names_admin_menu[1]:
                await AdminCreatePost.post.set()
                await callback_query.message.edit_text('Отправте пост')

            elif callback_query.data == self.names_admin_menu[2]:
                file = InputFile('logging.log')

                if self.logger_message_id:
                    await self.bot.delete_message(callback_query.message.chat.id, self.logger_message_id)

                text = await callback_query.message.answer_document(file)
                self.logger_message_id = text.message_id

        await callback_query.answer()

    async def exitAdmin(self, callback_query: types.CallbackQuery):
        if callback_query.message.chat.type == 'private' \
                and callback_query.message.chat.username == self.admin_username:

            text_admin = await self.__templateText_cmdAdmin(callback_query.message.chat.id)
            await callback_query.message.edit_text(text_admin, reply_markup=self.admin_menu_inline)

        await callback_query.answer()

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.cmdAdmin, commands=['admin'])

        dp.register_callback_query_handler(self.cmdAdminMenu, Text(equals=self.names_admin_menu, ignore_case=True))

        dp.register_callback_query_handler(self.exitAdmin, Text(equals=self.nameExit_admin_menu, ignore_case=True))