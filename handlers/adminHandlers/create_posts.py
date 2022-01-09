from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.adminHandlers.init import InitAdmin
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from classes.Keyboard import Keyboard
from datetime import datetime
from aiogram import Dispatcher, types
from classes.db import DB
import logging
import json


class CreatePost(InitAdmin):
    def __init__(self, db: DB, admin_chat_id: str, keyboards: Keyboard):
        super(CreatePost, self).__init__(admin_chat_id)

        self.log_create_post = logging.getLogger('create_post')
        self.db = db
        self.keyboards = keyboards

        self.admin_menu_create_buttons_ok = [
            {'title': 'Продолжить', 'callback_data': 'create_button_ok', 'url': False}
        ]

    class FSMCreatePost(StatesGroup):
        post = State()
        buttons = State()
        time = State()

    async def __stateMedia(self, message: types.Message,  text: str, media: str, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = text
            data['media'] = media
            data['buttons'] = list()
        await self.FSMCreatePost.next()

        buttons = self.db.selectsButtons()
        if buttons:
            buttons_reply_markup = list()
            for item in buttons:
                item['url'] = False
                item['callback_data'] = item['title']
                buttons_reply_markup.append(item)

            buttons_reply_markup = self.keyboards.edit_item_list(buttons_reply_markup, 3)
            buttons_reply_markup.append(*self.admin_menu_create_buttons_ok)
            await message.answer('Выберите кнопки', reply_markup=self.keyboards.inline(buttons_reply_markup))
        else:
            await message.answer('Выберите кнопки (Нет созданых кнопак)',
                                 reply_markup=self.keyboards.inline(self.admin_menu_create_buttons_ok))

    async def callbackDataCreatePost(self, callback_query: types.CallbackQuery):
        if self.chAdmin(callback_query.message):
            await self.FSMCreatePost.post.set()
            await callback_query.message.edit_text('Отправьте свой пост')
        await callback_query.answer()

    async def CreatePostText(self, message: types.Message, state: FSMContext):
        if self.chAdmin(message):
            await self.__stateMedia(message, message.text, 'false:none', state)

    async def CreatePostPhoto(self, message: types.Message, state: FSMContext):
        if self.chAdmin(message):
            if message.caption:
                await self.__stateMedia(message, message.caption, f'photo:{message.photo[0].file_id}', state)

    async def CreatePostVideo(self, message: types.Message, state: FSMContext):
        if self.chAdmin(message):
            if message.caption:
                await self.__stateMedia(message, message.caption, f'video:{message.video.file_id}', state)

    async def callbackDataAppendButtonsCreatePost(self, callback_query: types.CallbackQuery, state: FSMContext):
        if self.chAdmin(callback_query.message):
            async with state.proxy() as data:
                if callback_query.data not in data['buttons']:
                    data['buttons'].append(callback_query.data)
                    await callback_query.answer(f"Кнопка успешно добавлена - {callback_query.data}")
                else:
                    data['buttons'].remove(callback_query.data)
                    await callback_query.answer(f"Кнопка успешно удалина - {callback_query.data}")
        await callback_query.answer()

    async def callbackDataCreateButtonOK(self, callback_query: types.CallbackQuery, state: FSMContext):
        if self.chAdmin(callback_query.message):
            async with state.proxy() as data:
                if len(data['buttons']) <= 0:
                    data['buttons'] = 'false'
            await self.FSMCreatePost.next()
            await callback_query.message.edit_text('Отправьте время публикации в формате YYYY HH:MM:SS')
        await callback_query.answer()

    async def CreatePostTime(self, message: types.Message, state: FSMContext):
        if self.chAdmin(message):
            try:
                datetime.strptime(message.text, '%d.%m.%Y %H:%M:%S')
                async with state.proxy() as data:
                    data['time'] = message.text

                if data['buttons'] != 'false':
                    arr_button = list()
                    for item in data['buttons']:
                        button = self.db.selectButtonTitle(item)
                        if button:
                            button['callback_data'] = False
                        arr_button.append(button)
                    arr_button = json.dumps(arr_button)
                else:
                    arr_button = 'false'

                insert = self.db.insertPosts(data['text'], '0', data['time'], data['media'], arr_button)
                if insert:
                    await state.finish()
                    await message.answer("Пост успешно добавлен")
                else:
                    await message.answer("На данное время пост уже создан введите другое время")
            except ValueError:
                self.log_create_post.error("Incorrect data format, should be DD.MM.YYYY HH:MM:SS")

    def registerHandlersCreatePost(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.callbackDataCreatePost, Text(equals='create_post', ignore_case=True))
        dp.register_message_handler(self.CreatePostText, content_types='text', state=self.FSMCreatePost.post)
        dp.register_message_handler(self.CreatePostPhoto, content_types='photo', state=self.FSMCreatePost.post)
        dp.register_message_handler(self.CreatePostVideo, content_types='video', state=self.FSMCreatePost.post)

        dp.register_callback_query_handler(self.callbackDataAppendButtonsCreatePost,
                                           Text(equals=self.db.selectButtonsTitle(), ignore_case=True),
                                           state=self.FSMCreatePost.buttons)

        dp.register_callback_query_handler(self.callbackDataCreateButtonOK,
                                           Text(equals='create_button_ok', ignore_case=True),
                                           state=self.FSMCreatePost.buttons)

        dp.register_message_handler(self.CreatePostTime, content_types='text', state=self.FSMCreatePost.time)