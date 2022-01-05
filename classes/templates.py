from jinja2 import Environment, Template
from aiogram import Bot


class Templates:
    def __init__(self, bot: Bot, env: Environment):
        self.bot = bot
        self.env = env

    @staticmethod
    def templates_text_only(text: str, objects: dict = None):
        return Template(text).render(objects)

    def templates_text(self, file: str, objects: dict = None):
        start_text = self.env.get_template(file)
        if objects:
            return start_text.render(objects)
        return start_text.render()

    async def temUser(self, id_chat: str):
        chat = await self.bot.get_chat(id_chat)
        return chat

