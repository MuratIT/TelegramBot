from sqlalchemy import Column, Integer, String

from classes.classes_db import InitDB

db = InitDB()


class UsersDB(db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    id_chat = Column(String(255), nullable=True)
    blocked = Column(Integer, nullable=True)

    def __init__(self, id_chat: str, blocked: int):
        self.id_chat = id_chat
        self.blocked = blocked