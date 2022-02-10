from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminCreatePost(StatesGroup):
    post = State()
    button = State()
    title = State()
    url = State()
    continues = State()
    time = State()