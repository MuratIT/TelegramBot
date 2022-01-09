from classes.classes_db.init_db import InitDB
import logging


class UsersDB(InitDB):
    def __init__(self, name: str):
        super(UsersDB, self).__init__(name)
        self.log_users_db = logging.getLogger('users_db')

        self.connectExecute("""CREATE TABLE IF NOT EXISTS users(
                               id_user VARCHAR(255) NOT NULL,
                               blocked VARCHAR(255) NOT NULL,
                               PRIMARY KEY(id_user));
                            """)

    def insertUsers(self, id_user: str, blocked: str):
        select = self.selectUsers(id_user)
        if not select:
            sql = 'INSERT INTO users (id_user, blocked) VALUES (?, ?)'
            temp = (id_user, blocked)
            self.connectExecute(sql=sql, temp=temp)
            return True
        return False

    def updateUsersBlocked(self, id_user: str, blocked: str):
        sql = 'UPDATE users SET blocked=? WHERE id_user=?'
        temp = (blocked, id_user)
        self.connectExecute(sql=sql, temp=temp, fetch='fetchone')

    def selectUsers(self, id_user: str):
        sql = 'SELECT * FROM users WHERE id_user=?'
        temp = (id_user,)
        return self.connectExecute(sql=sql, temp=temp, commit=False, fetch='fetchone')

    def selectUsersCount(self, blocked: str):
        sql = 'SELECT count() as count FROM users WHERE blocked=?'
        temp = (blocked,)
        return self.connectExecute(sql=sql, temp=temp, commit=False, fetch='fetchone')

    def selectsUsers(self):
        sql = 'SELECT * FROM users'
        return self.connectExecute(sql=sql, commit=False, fetch='fetchall')

    def deleteUser(self, id_user: str):
        if self.selectUsers(id_user):
            sql = 'DELETE FROM users WHERE id_user=?'
            temp = (id_user,)
            self.connectExecute(sql=sql, temp=temp)