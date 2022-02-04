import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class InitDB:
    Base = declarative_base()

    def __init__(self, name: str = 'dataBase'):
        self.name = f'{name}.sqlite'

        self.__engine = create_engine(f'sqlite:///{self.name}')
        self.__session = sessionmaker(bind=self.__engine)

    def createDatabase(self):
        if not os.path.exists(self.name):
            self.Base.metadata.create_all(self.__engine)

    def sessionDB(self, object_db: object):
        def wrapper(func):
            session_db = self.__session()
            query = session_db.query(object_db)
            func_query = func(object_db, query, session_db)
            session_db.close()
            return func_query
        return wrapper