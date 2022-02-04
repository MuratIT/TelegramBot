from sqlalchemy import Column, Integer, String, Text

from classes.classes_db import InitDB

db = InitDB()


class PostDB(db.Base):
    __tablename__ = "posts"
    text = Column(Text, nullable=True)
    media = Column(Text, nullable=True)
    reply_markup = Column(Text, nullable=True)
    checked = Column(Integer, nullable=True)
    time = Column(String(255), primary_key=True)

    def __init__(self, text: str, media: str, reply_markup: str, checked: int, time: str):
        self.text = text
        self.media = media
        self.reply_markup = reply_markup
        self.checked = checked
        self.time = time