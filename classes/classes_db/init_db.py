import sqlite3
import logging


class InitDB:
    def __init__(self, name: str):
        self.log_init_db = logging.getLogger('init_db')
        self.__name = name

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def __fetchReturn(aw: any, formats: str):
        if formats == 'fetchone':
            return aw.fetchone()
        elif formats == 'fetchall':
            aw_arr = list()
            for item in aw.fetchall():
                aw_arr.append(item)
            return aw_arr
        return None

    def connectExecute(self, sql: str, temp: tuple = tuple(), commit: bool = True, fetch: str = None):
        with sqlite3.connect(f'{self.__name}.db') as connect:
            try:
                connect.row_factory = self.dict_factory

                cursor = connect.cursor()
                aw = cursor.execute(sql, temp)
                if commit:
                    connect.commit()

                return self.__fetchReturn(aw, fetch)
            except sqlite3.DatabaseError as err:
                self.log_init_db.error(err)
