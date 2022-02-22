from asyncio import get_event_loop, set_event_loop
from datetime import datetime
import logging
import asyncio
import random
import json

from aiogram.types import InputFile, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from aiogram.utils.exceptions import BotBlocked, BotKicked, ChatNotFound, UserDeactivated, TelegramAPIError
from aiogram import Bot

from classes.templates import Templates
from classes.Keyboard import Keyboard
from classes.classes_db import InitDB
from classes.classes_db import UsersDB
from classes.classes_db import PostDB
from classes.classes_db import ChannelChatDB
from classes.functions import Functions


class Broadcaster(Functions):
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        
        super(Broadcaster, self).__init__(bot, db, loop, Keyboards, temp)

        self.log = logging.getLogger('Broadcaster')

        self.db = db
        self.bot = bot
        self.loop = loop
        self.Keyboards = Keyboards
        self.temp = temp

    @staticmethod
    def __group_list(expansion: str, expansion_media: list, expansion_photo: list, expansion_video: list,
                     expansion_audio: list, expansion_document: list, item_type: str, id_media: list,
                     caption: str, item: any):
        if expansion in expansion_media:
            if item_type in expansion_photo:
                id_media.append(InputMediaPhoto(item,
                                                caption=caption if len(id_media) == 0 else None))
            elif item_type in expansion_video:
                id_media.append(InputMediaVideo(item,
                                                caption=caption if len(id_media) == 0 else None))

        elif expansion in expansion_audio:
            if item_type in expansion_audio:
                id_media.append(InputMediaAudio(item,
                                                caption=caption if len(id_media) == 0 else None))

        elif expansion in expansion_document:
            if item_type in expansion_document:
                id_media.append(InputMediaDocument(item,
                                                   caption=caption if len(id_media) == 0 else None))

    def group_input_file(self, media_files: list, caption: str):
        id_media = list()
        name = media_files[0]

        if media_files[0] == 'group':
            expansion = media_files[1].split('/', 1)[0].lstrip()

            expansion_photo = ['photo']
            expansion_video = ['video']
            expansion_media = [*expansion_photo, *expansion_video]

            expansion_audio = ['audio']
            expansion_document = ['document']

            for item in media_files:
                if item != name:
                    item_type = item.split('/', 1)[0].lstrip()
                    item_id = item.split('/', 1)[1].lstrip()

                    self.__group_list(expansion, expansion_media, expansion_photo, expansion_video,
                                      expansion_audio, expansion_document, item_type, id_media, caption, item_id)

            return 'group', id_media

        elif media_files[0] == 'file/group':
            expansion = media_files[1].split('.', 1)[1].lstrip()

            expansion_photo = ['jpg', 'png']
            expansion_video = ['mp4']
            expansion_media = [*expansion_photo, *expansion_video]

            expansion_audio = ['mp3']
            expansion_document = ['txt', 'doc', 'xls', 'pdf']

            for item in media_files:
                if item != name:
                    item_type = item.split('.', 1)[1].lstrip()

                    self.__group_list(expansion, expansion_media, expansion_photo, expansion_video, expansion_audio,
                                      expansion_document, item_type, id_media, caption, InputFile(item))

            return 'group', id_media

        return 'false', 'none'

    def input_file(self, media: str, caption: str = None):
        media_files = media.split(':')
        if len(media_files) == 2:
            media, id_media = media_files

            if media == 'file/photo':
                media, id_media = 'photo', InputFile(id_media)
            elif media == 'file/video':
                media, id_media = 'video', InputFile(id_media)
            elif media == 'file/document':
                media, id_media = 'document', InputFile(id_media)
            elif media == 'file/audio':
                media, id_media = 'audio', InputFile(id_media)

            return media, id_media

        elif len(media_files) > 2:
            return self.group_input_file(media_files, caption)

        return 'false', 'none'

    def chJson(self, string: str):
        try:
            return json.loads(string)
        except Exception as e:
            self.log.error(e)
            return list()

    def reply_markup(self, reply_markup: str):
        if reply_markup != '0':
            reply_markup = self.Keyboards.inline(self.chJson(reply_markup))
            return reply_markup

    async def send(self, id_chat: str, message: str, media: str = None, id_media: str or InputFile = None,
                   reply_markup: Keyboard.inline = None):
        try:
            if media == 'photo':
                await self.bot.send_photo(id_chat, id_media, caption=message, reply_markup=reply_markup)
            elif media == 'video':
                await self.bot.send_video(id_chat, id_media, caption=message, reply_markup=reply_markup)
            elif media == 'document':
                await self.bot.send_document(id_chat, id_media, caption=message, reply_markup=reply_markup)
            elif media == 'audio':
                await self.bot.send_audio(id_chat, id_media, caption=message, reply_markup=reply_markup)
            elif media == 'group':
                await self.bot.send_media_group(id_chat, id_media)
            else:
                await self.bot.send_message(id_chat, message, reply_markup=reply_markup)
        except BotBlocked:
            self.addUser(id_chat, 1)

        except BotKicked:
            self.addChannelChat(id_chat, 1)

        except ChatNotFound:
            self.deleteUser(id_chat)
            self.deleteChannelChat(id_chat)

        except UserDeactivated:
            self.deleteUser(id_chat)
            self.deleteChannelChat(id_chat)

        except TelegramAPIError as TAPI:
            self.log.error(TAPI)

    async def __sendUsersAll(self, text: str, media: str, reply_markup: str):
        media, id_media = self.input_file(media, text)

        with self.db.session_scope() as session:
            select = session.query(UsersDB).all()

            for item in select:
                if item.blocked == 0:
                    text = self.temp.templates_text_only(text, await self.temp.temUser(item.id_chat))
                    await self.send(item.id_chat, text, media, id_media, self.reply_markup(reply_markup))

    async def __sendChannelChat(self, text: str, media: str, reply_markup: str):
        media, id_media = self.input_file(media, text)

        with self.db.session_scope() as session:
            select = session.query(ChannelChatDB).all()

            for item in select:
                if item.blocked == 0:
                    await self.send(item.id_channel_chat, text, media, id_media, self.reply_markup(reply_markup))

    async def __broadcaster(self):
        while True:
            await asyncio.sleep(0.1)
            time = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

            with self.db.session_scope() as session:
                select = session.query(PostDB).filter(PostDB.time == time).first()

                if select:
                    if select.checked == 0:
                        await self.__sendUsersAll(select.text, select.media, select.reply_markup)
                        session.query(PostDB).filter(PostDB.time == select.time).update(
                            {'checked': 1, 'time': f'usersDB:id:{random.randint(2344, 234432)}'})
                        session.commit()

    async def __broadcasterChannelChat(self):
        while True:
            await asyncio.sleep(0.1)
            time = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
            with self.db.session_scope() as session:
                select = session.query(PostDB).filter(PostDB.time == time).first()

                if select:
                    if select.checked == 2:
                        await self.__sendChannelChat(select.text, select.media, select.reply_markup)
                        session.query(PostDB).filter(PostDB.time == select.time).update(
                            {'checked': 3, 'time': f'ChannelChatDB:id:{random.randint(2344, 234432)}'})
                        session.commit()

    async def run(self):
        self.loop.create_task(self.__broadcaster())
        self.loop.create_task(self.__broadcasterChannelChat())