import os
from contextlib import contextmanager

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
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

    @contextmanager
    def session_scope(self):
        session = self.__session()
        try:
            yield session
            session.commit()
        except ValueError:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def select_session(self, objects: object):
        session = Session(self.__engine).execute(select(objects))
        try:
            yield session
        except ValueError:
            session.rollback()
            raise
        finally:
            session.close()