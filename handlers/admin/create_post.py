import json

from asyncio import get_event_loop, set_event_loop

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from classes.classes_db import InitDB
from classes.classes_db import PostDB
from classes.templates import Templates
from classes.Keyboard import Keyboard
from classes.functions import Functions
from classes.gettext import getText
from classes.states_group import AdminCreatePost


class CreatePost(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        super(CreatePost, self).__init__(bot, db, loop, Keyboards, temp)

        self.db = db
        self.keyboard = Keyboards
        self.temp = temp

    @staticmethod
    async def __StatePostObject(state: FSMContext, text: str, photo: str = "false", video: str = "false",
                                audio: str = "false", document: str = "false"):
        if text:
            async with state.proxy() as data:
                data['text'] = text
                data['photo'] = photo
                data['video'] = video
                data['audio'] = audio
                data['document'] = document
            return True
        return False

    async def __createPost(self, message: types.Message):
        await AdminCreatePost.next()
        keyboard = self.keyboard.loadKeyboard('create_buttons_admin')[0]
        await message.answer(getText('create_button'), reply_markup=self.keyboard.inline(keyboard))

    async def createPost(self, message: types.Message, state: FSMContext):
        text = await self.__StatePostObject(state, message.text)
        if text:
            await self.__createPost(message)
        else:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))

    async def createPostPhoto(self, message: types.Message, state: FSMContext):
        text = await self.__StatePostObject(state, message.caption, photo=message.photo[0].file_id)
        if text:
            await self.__createPost(message)
        else:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))

    async def createPostVideo(self, message: types.Message, state: FSMContext):
        text = await self.__StatePostObject(state, message.caption, video=message.video.file_id)
        if text:
            await self.__createPost(message)
        else:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))

    async def createPostAudio(self, message: types.Message, state: FSMContext):
        text = await self.__StatePostObject(state, message.caption, audio=message.audio.file_id)
        if text:
            await self.__createPost(message)
        else:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))

    async def createPostDocument(self, message: types.Message, state: FSMContext):
        text = await self.__StatePostObject(state, message.caption, document=message.document.file_id)
        if text:
            await self.__createPost(message)
        else:
            await message.delete()
            await message.answer(getText('send_post_error_validators'))

    async def createButtons(self, message: types.CallbackQuery, state: FSMContext):
        if message.data == 'createButtonYes':
            await AdminCreatePost.next()
            await message.message.edit_text(getText('title_button'))

        elif message.data == 'createButtonNo':
            async with state.proxy() as data:
                data['buttons'] = "false"

            await AdminCreatePost.time.set()
            admin_exit = self.keyboard.loadKeyboard('cancellation')[0]
            await message.message.edit_text(getText('time'), reply_markup=self.keyboard.inline(admin_exit))

        await message.answer()

    async def createPostTime(self, message: types.Message, state: FSMContext):
        with self.db.session_scope() as session:
            select = session.query(PostDB).filter(PostDB.time == message.text).first()
            if not select:
                async with state.proxy() as data:
                    temp_media = str()
                    for key, value in data.items():
                        if value != 'false' and key != 'text' and key != 'buttons':
                            temp_media += f'{key}:{value}'

                    if len(temp_media) == 0:
                        temp_media = 'false:none'

                    buttons = False
                    if data['buttons'] != 'false':
                        buttons = json.dumps(data['buttons'], ensure_ascii=False)

                    post = PostDB(data['text'], temp_media, buttons, 0, message.text)

                    session.add(post)
                    session.commit()

                await state.finish()
                await message.answer(getText('post_successfully'))
            else:
                await message.answer(getText('time_error_repeated'))

    def registerHandlers(self, dp: Dispatcher):
        dp.register_message_handler(self.createPost, content_types='text',
                                    state=AdminCreatePost.post, is_admin=True, chat_private=True)

        dp.register_message_handler(self.createPostPhoto, content_types='photo',
                                    state=AdminCreatePost.post, is_admin=True, chat_private=True)

        dp.register_message_handler(self.createPostVideo, content_types='video',
                                    state=AdminCreatePost.post, is_admin=True, chat_private=True)

        dp.register_message_handler(self.createPostAudio, content_types='audio',
                                    state=AdminCreatePost.post, is_admin=True, chat_private=True)

        dp.register_message_handler(self.createPostDocument, content_types='document',
                                    state=AdminCreatePost.post, is_admin=True, chat_private=True)

        dp.register_callback_query_handler(self.createButtons,
                                           Text(equals=self.keyboard.loadKeyboard('create_buttons_admin')[1],
                                                ignore_case=True),
                                           state=AdminCreatePost.button, is_admin=True, chat_private=True)

        dp.register_message_handler(self.createPostTime, content_types='text', state=AdminCreatePost.time,
                                    is_admin=True, chat_private=True, is_time=True)
