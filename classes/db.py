from classes.classes_db.buttons_db import ButtonsDB
from classes.classes_db.users_db import UsersDB
from classes.classes_db.posts_db import PostsDB


class DB(UsersDB, PostsDB, ButtonsDB):
    def __init__(self, name: str):
        super(DB, self).__init__(name)