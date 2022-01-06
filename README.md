# **Template for developing telegram bot**
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/aiogram) [![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-5.6-blue.svg?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api)

| Libraries / Libraries | Installation Guide | github / website |
|:----------------:|:---------:|:----------------:|
| aiogram | pip install aiogram | [aiogram](https://github.com/aiogram/aiogram) |
| Jinja2 | pip install Jinja2 | [Jinja2](https://github.com/pallets/jinja) |
___
## File Structure
- `init.py`
- `Telegram_Bot.py`
- `text_templates`
    - `start.txt`
- `handlers`
    - `__init__.py`
    - `client.py`
    - `errors.py`
- `classes`
    - `__init__.py`
    - `Broadcaster.py`
    - `db.py`
    - `Keyboard.py`
    - `templates.py`
___
### `init.py`
**The bot initialization file into which you import all modules from the classes folder, as well as the main libraries and modules for the bot to work**
### `Telegram_Bot.py`
**The main startup file is the file we are launching. In which we import everything from a file init.py and from modules in the handlers folder**
___
### `text_templates`
**This folder is intended for files from which a certain text is taken, which subsequently passes through the Jinja2 template engine.**
### `handlers`
**All files with bot event handlers are stored in this folder**
## `classes`
**Modules for stable operation of the bot are stored in this folder, and you can also add your own modules there, which later you will just need to connect and thus remove the functionality.**
___
## The bot already knows how to
- **Remembers users in the database, namely their ID**
- **Added a mailing list for all active bot users (beta version)**
- **It has the most popular template engine**
- **The bot also has a built-in logger to log in to the file**
