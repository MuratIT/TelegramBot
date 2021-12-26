import sqlite3
import logging


class DB:
    def __init__(self, name: str):
        self.log = logging.getLogger('DB')

        self.connect = sqlite3.connect(f'{name}.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                               id_user VARCHAR(255) NOT NULL,
                               blocked VARCHAR(255) NOT NULL,
                               PRIMARY KEY(id_user));
                            """)

        self.connect.commit()

    def __format(self, query: tuple):
        names = [description[0] for description in self.cursor.description]
        return dict(zip(names, query))

    def insertUsers(self, id_user: str, blocked: str):
        select = self.selectUsers(id_user)
        if not select:
            self.cursor.execute('INSERT INTO users (id_user, blocked) VALUES (?, ?)', (id_user, blocked))
            self.connect.commit()
            return True
        return False

    def updateUsersBlocked(self, id_user: str, blocked: str):
        self.cursor.execute('UPDATE users SET blocked=? WHERE id_user=?', (blocked, id_user))
        self.connect.commit()

    def selectUsers(self, id_user: str):
        select = self.cursor.execute('SELECT * FROM users WHERE id_user=?', (id_user,)).fetchone()
        if select:
            return self.__format(select)

    def deleteUser(self, id_user: str):
        if self.selectUsers(id_user):
            self.cursor.execute('DELETE FROM users WHERE id_user=?', (id_user,))
            self.connect.commit()