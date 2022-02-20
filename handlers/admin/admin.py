from asyncio import get_event_loop, set_event_loop

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from classes.classes_db import InitDB
from classes.classes_db import UsersDB
from classes.templates import Templates
from classes.Keyboard import Keyboard
from classes.functions import Functions
from classes.gettext import getText
from classes.states_group import AdminCreatePost


class Admin(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        super(Admin, self).__init__(bot, db, loop, Keyboards, temp)

        self.db = db
        self.keyboard = Keyboards
        self.temp = temp

        self.admin_menu = ['Статистика', 'Создать пост'],\
                          ['statisticsAdmin', 'createPostAdmin']

        self.admin_exit = self.keyboard.loadKeyboard('exit')
        self.admin_cancellation = self.keyboard.loadKeyboard('cancellation')

        self.keyboard.createInlineDynamicKeyboard(db, 'admin', self.admin_menu[0], callback_data=self.admin_menu[1])

    async def cmdAdminTemp(self, message: types.Message):
        tem = await self.temp.temUser(message.chat.id)
        text_admin = self.temp.templates_text('admin.txt', tem)
        keyboard = self.keyboard.loadDynamicKeyboard(self.db, 'admin')
        return text_admin, keyboard

    async def cmdAdmin(self, message: types.Message):
        print(self.temp_object)
        text_admin, keyboard = await self.cmdAdminTemp(message)
        await message.answer(text_admin, reply_markup=self.keyboard.inline(keyboard, 2))

    async def CallbackAdmin(self, message: types.CallbackQuery):
        if message.data == self.admin_menu[1][0]:
            with self.db.session_scope() as session:
                users_query = session.query(UsersDB)
                self.temp_object['all_users'] = users_query.count()
                self.temp_object['active_users'] = users_query.filter(UsersDB.blocked == 0).count()
                self.temp_object['passive_users'] = users_query.filter(UsersDB.blocked == 1).count()

            tem = self.temp.templates_text('statistics.txt', self.temp_object)

            await message.message.edit_text(tem, reply_markup=self.keyboard.inline(self.admin_exit[0]))
        elif message.data == self.admin_menu[1][1]:
            await AdminCreatePost.post.set()
            await message.message.edit_text(getText('send_post'),
                                            reply_markup=self.keyboard.inline(self.admin_cancellation[0]))

        await message.answer()

    async def cmdExit(self, message: types.CallbackQuery):
        text_admin, keyboard = await self.cmdAdminTemp(message.message)
        await message.message.edit_text(text_admin, reply_markup=self.keyboard.inline(keyboard, 2))

    @staticmethod
    async def cancellationAdmin(message: types.CallbackQuery, state: FSMContext):
        await state.finish()
        await message.message.edit_text(getText('post_successfully_exit'))

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.cmdAdmin, commands=['admin'], is_admin=True, chat_private=True)

        dp.register_callback_query_handler(self.CallbackAdmin, is_menu=[self.db, self.keyboard, 'admin'],
                                           is_admin=True, chat_private=True)

        dp.register_callback_query_handler(self.cmdExit, Text(equals=self.admin_exit[1], ignore_case=True),
                                           is_admin=True, chat_private=True)

        dp.register_callback_query_handler(self.cancellationAdmin,
                                           Text(equals=self.admin_cancellation[1], ignore_case=True), is_admin=True,
                                           chat_private=True, state="*")
