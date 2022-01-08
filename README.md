# **Template for telegram bot development**
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/aiogram) [![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-5.6-blue.svg?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api)

| Library | installation Guide | web site | 
|:----------------:|:---------:|:----------------:| 
| aiogram | pip install aiogram | [aiogram](https://pypi.python.org/pypi/aiogram) |
| Jinja2 | pip install Jinja2 | [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) |
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
    - `classes_db`
___
### `init.py`
**The bot initialization file into which you import all modules from the classes folder, as well as the main libraries and modules for the bot to work**
### `Telegram_Bot.py`
**The main startup file is the file we are launching. In which we import everything from a file init.py and modules in the handlers folder**
___
### `text_templates`
**This folder is intended for files from which a certain text is taken, which subsequently passes through the Jinja2 template engine.**
### `handlers`
**All files with bot event handlers are stored in this folder**
### `classes`
- **Modules for the stable operation of the bot are stored in this folder, and you can also add your own modules, which later you will just need to plug and thus add functionality.** 
- ### `classes_db` 
  - **This folder contains the class files to create the tables and methods of interacting with the database tables**

___
## The bot already knows how to do:
- **Remembers users in the database, namely their ID**
- **There is a built-in method of mailing by time (beta version)**
- **It has the most popular Jinja2 template engine**
- **The bot also logs all events to a file**