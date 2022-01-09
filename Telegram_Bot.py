from init import dp, db, env, Keyboards, temp, loop, broadcaster, ADMIN_CHAT_ID
from aiogram import executor, Dispatcher
from handlers.client import Client
from handlers.errors import Errors
from handlers.admin import Admin
import logging


log = logging.getLogger('Telegram_Bot')


async def on_startup(DP: Dispatcher):
    error = Errors(db=db)
    admin = Admin(db=db, admin_chat_id=ADMIN_CHAT_ID, temp=temp, keyboards=Keyboards)
    client = Client(db=db, env=env, keyboards=Keyboards, temp=temp, error=error)

    await broadcaster.run()
    error.registerHandlers(DP)
    admin.registerHandlers(DP)
    client.registerHandlers(DP)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, loop=loop, skip_updates=True, on_startup=on_startup)