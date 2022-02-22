import os

from asyncio import get_event_loop, set_event_loop

from aiogram import Bot

from classes.classes_db import InitDB
from classes.classes_db import UsersDB
from classes.classes_db import ChannelChatDB
from classes.Keyboard import Keyboard
from classes.templates import Templates


class Functions:
    def __init__(self, bot: Bot, db: InitDB,
                 loop: get_event_loop or set_event_loop,
                 Keyboards: Keyboard, temp: Templates):
        self.db = db
        self.bot = bot
        self.loop = loop
        self.Keyboards = Keyboards
        self.temp = temp

        self.admin_username = os.environ.get('ADMIN_USERNAME')

        self.temp_object = dict()

    def deleteUser(self, id_chat: str):
        with self.db.session_scope() as session:
            session.query(UsersDB).filter(UsersDB.id_chat == id_chat).delete()

    def addUser(self, id_chat: str, blocked: int):
        with self.db.session_scope() as session:
            select = session.query(UsersDB).filter(UsersDB.id_chat == id_chat).first()
            if not select:
                user = UsersDB(id_chat, blocked)
                session.add(user)
            else:
                session.query(UsersDB).filter(UsersDB.id_chat == select.id_chat).update({'blocked': blocked})
            session.commit()

    def deleteChannelChat(self, id_chat: str):
        with self.db.session_scope() as session:
            session.query(ChannelChatDB).filter(ChannelChatDB.id_channel_chat == id_chat).delete()

    def addChannelChat(self, id_chat: str, blocked: int):
        with self.db.session_scope() as session:
            select = session.query(ChannelChatDB).filter(ChannelChatDB.id_channel_chat == id_chat).first()
            if not select:
                user = ChannelChatDB(id_chat, blocked)
                session.add(user)
            else:
                session.query(ChannelChatDB).filter(ChannelChatDB.id_channel_chat == select.id_channel_chat).update(
                    {'blocked': blocked})
            session.commit()