from classes.classes_db.init_db import InitDB
import logging


class PostsDB(InitDB):
    def __init__(self, name: str):
        super(PostsDB, self).__init__(name)
        self.log_posts_db = logging.getLogger('posts_db')

        self.connectExecute("""CREATE TABLE IF NOT EXISTS posts(
                               text TEXT NOT NULL,
                               media TEXT NOT NULL,
                               reply_markup TEXT NOT NULL,
                               checked VARCHAR(255) NOT NULL,
                               time VARCHAR(255) NOT NULL,
                               PRIMARY KEY(time));
                            """, formats='')

    def insertPosts(self, text: str, checked: str, time: str, media: str = 'false:none', reply_markup: str = 'false'):
        select = self.selectPosts(time)
        if not select:
            sql = 'INSERT INTO posts (text, media, reply_markup, checked, time) VALUES (?, ?, ?, ?, ?)'
            temp = (text, media, reply_markup, checked, time)
            self.connectExecute(sql=sql, temp=temp, formats=str())
            return True
        return False

    def updatePostsChecked(self, checked: str, time: str):
        sql = 'UPDATE posts SET checked=? WHERE time=?'
        temp = (checked, time)
        self.connectExecute(sql=sql, temp=temp, formats=str())

    def selectPosts(self, time: str):
        sql = 'SELECT * FROM posts WHERE time=?'
        temp = (time,)
        return self.connectExecute(sql=sql, temp=temp, commit=False, formats='fetchone')

    def deletePosts(self, time: str):
        if self.selectPosts(time):
            sql = 'DELETE FROM posts WHERE time=?'
            temp = (time,)
            self.connectExecute(sql=sql, temp=temp, formats=str())