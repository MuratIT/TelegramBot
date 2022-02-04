import logging

from aiogram import executor, Dispatcher

from init import dp, db, env, Keyboards, temp, loop, broadcaster
from handlers.client import Client
from handlers.errors import Errors


log = logging.getLogger('Telegram_Bot')


async def on_startup(DP: Dispatcher):
    error = Errors(db=db)
    client = Client(db=db, env=env, keyboards=Keyboards, temp=temp, error=error)

    await broadcaster.run()
    error.registerHandlers(DP)
    client.registerHandlers(DP)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, loop=loop, skip_updates=True, on_startup=on_startup)