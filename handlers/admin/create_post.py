import os
import json
import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from classes.gettext import getText
from classes.classes_db import InitDB
from classes.classes_db import PostDB
from classes.Keyboard import Keyboard
from classes.templates import Templates
from classes.states_group import AdminCreatePost


class CreatePost:
    def __init__(self, db: InitDB, keyboard: Keyboard, temp: Templates):
        self.db = db
        self.keyboard = keyboard
        self.temp = temp
        self.admin_username = os.environ.get('ADMIN_USERNAME')

        self.stat_text_button = getText('create_button')

        self.keyboard_button_names = ['Да', 'Нет']
        self.keyboard_button_object = self.keyboard.InlineMenu(self.keyboard_button_names)
        self.keyboard_button = self.keyboard.inline(self.keyboard_button_object)

    @staticmethod
    async def __chekText(message: types.Message):
        if not message.caption:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))
            return False
        return True

    @staticmethod
    async def __chekTime(message: types.Message):
        try:
            datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M:%S')
            return True
        except ValueError:
            await message.delete()
            await message.answer(getText('time_error_validators'))
            return False

    @staticmethod
    async def __StatePostObject(text: str, photo: str, video: str, audio: str, document: str, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = text
            data['photo'] = photo
            data['video'] = video
            data['audio'] = audio
            data['document'] = document

    async def CreatePost(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:
            await self.__StatePostObject(message.text, 'false', 'false', 'false', 'false', state)
            await AdminCreatePost.next()
            await message.answer(self.stat_text_button, reply_markup=self.keyboard_button)

    async def CreatePostPhoto(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:
            if await self.__chekText(message):
                await self.__StatePostObject(message.caption, message.photo[0].file_id,
                                             'false', 'false', 'false', state)
                await AdminCreatePost.next()
                await message.answer(self.stat_text_button, reply_markup=self.keyboard_button)

    async def CreatePostVideo(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:

            if await self.__chekText(message):
                await self.__StatePostObject(message.caption, 'false', message.video.file_id, 'false', 'false', state)
                await AdminCreatePost.next()
                await message.answer(self.stat_text_button, reply_markup=self.keyboard_button)

    async def CreatePostAudio(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:
            if await self.__chekText(message):
                await self.__StatePostObject(message.caption, 'false', 'false', message.audio.file_id, 'false', state)
                await AdminCreatePost.next()
                await message.answer(self.stat_text_button, reply_markup=self.keyboard_button)

    async def CreatePostDocument(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:
            if await self.__chekText(message):
                await self.__StatePostObject(message.caption,
                                             'false', 'false', 'false', message.document.file_id, state)
                await AdminCreatePost.next()
                await message.answer(self.stat_text_button, reply_markup=self.keyboard_button)

    async def CreateButton(self, CallbackQuery: types.CallbackQuery, state: FSMContext):
        if CallbackQuery.message.chat.type == 'private' \
                and CallbackQuery.message.chat.username == self.admin_username:

            if CallbackQuery.data == self.keyboard_button_names[0]:

                await AdminCreatePost.next()
                await CallbackQuery.message.edit_text(getText('title_button'))

            elif CallbackQuery.data == self.keyboard_button_names[1]:
                async with state.proxy() as data:
                    data['buttons'] = 'false'

                await AdminCreatePost.time.set()
                await CallbackQuery.message.edit_text(getText('time'))

        await CallbackQuery.answer()

    async def CreatePostTime(self, message: types.Message, state: FSMContext):
        if message.chat.type == 'private' \
                and message.chat.username == self.admin_username:
            if await self.__chekTime(message):
                async with state.proxy() as data:
                    temp_media = str()
                    for key, value in data.items():
                        if value != 'false' and key != 'text' and key != 'buttons':
                            temp_media += f'{key}:{value}'

                    buttons = False
                    if data['buttons'] != 'false':
                        buttons = json.dumps(data['buttons'])

                    if len(temp_media) == 0:
                        temp_media = 'false:none'

                    with self.db.session_scope() as session:
                        time = session.query(PostDB).filter(PostDB.time == message.text).first()
                        if not time:
                            post = PostDB(data['text'], temp_media, buttons, 0, message.text)
                            session.add(post)
                            session.commit()

                    if time:
                        await message.answer(getText('time_error_repeated'))
                    else:
                        await state.finish()
                        await message.answer(getText('post_successfully'))

    def registerHandlers(self, dp: Dispatcher):

        dp.register_message_handler(self.CreatePost, content_types="text", state=AdminCreatePost.post)
        dp.register_message_handler(self.CreatePostPhoto, content_types="photo", state=AdminCreatePost.post)
        dp.register_message_handler(self.CreatePostVideo, content_types="video", state=AdminCreatePost.post)
        dp.register_message_handler(self.CreatePostAudio, content_types="audio", state=AdminCreatePost.post)
        dp.register_message_handler(self.CreatePostDocument, content_types="document", state=AdminCreatePost.post)

        dp.register_callback_query_handler(self.CreateButton,
                                           Text(equals=self.keyboard_button_names, ignore_case=True),
                                           state=AdminCreatePost.button)

        dp.register_message_handler(self.CreatePostTime, content_types="text", state=AdminCreatePost.time)