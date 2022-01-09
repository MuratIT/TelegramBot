from classes.classes_db.init_db import InitDB
import logging


class ButtonsDB(InitDB):
    def __init__(self, name: str):
        super(ButtonsDB, self).__init__(name)
        self.log_buttons_db = logging.getLogger('buttons_db')

        self.connectExecute("""CREATE TABLE IF NOT EXISTS buttons(
                               title VARCHAR(255) NOT NULL,
                               url TEXT NOT NULL,
                               PRIMARY KEY(title));
                            """)

    def selectButtonTitle(self, title: str):
        sql = "SELECT * FROM buttons WHERE title=?"
        temp = (title,)
        select = self.connectExecute(sql=sql, temp=temp, commit=False, fetch='fetchone')
        if select:
            return select

    def selectsButtons(self):
        sql = "SELECT * FROM buttons"
        select = self.connectExecute(sql=sql, commit=False, fetch='fetchall')
        if select:
            return select

    def selectButtonsTitle(self, lists: list = True):
        sql = "SELECT title FROM buttons"
        select = self.connectExecute(sql=sql, commit=False, fetch='fetchall')
        if select:
            if lists:
                arr_title = list()
                for item in select:
                    arr_title.append(item['title'])
                return arr_title
            return select