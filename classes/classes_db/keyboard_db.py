from sqlalchemy import Column, Integer, String, Text

from classes.classes_db import InitDB

db = InitDB()


class KeyboardDB(db.Base):
    __tablename__ = "keyboards"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    reply_markup = Column(Text, nullable=True)

    def __init__(self, name: str, reply_markup: any):
        self.name = name
        self.reply_markup = reply_markup