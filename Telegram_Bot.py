from init import dp, db, env, Keyboards, temp
from aiogram import executor, Dispatcher
from handlers.client import Client
from handlers.errors import Errors
import logging


log = logging.getLogger('Telegram_Bot')


async def on_startup(DP: Dispatcher):
    error = Errors(db=db)
    client = Client(db=db, env=env, keyboards=Keyboards, temp=temp, error=error)

    error.registerHandlers(DP)
    client.registerHandlers(DP)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)