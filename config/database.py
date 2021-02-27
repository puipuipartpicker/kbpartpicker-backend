import os
from time import sleep
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.url import URL
from models._base import BaseModel


def _wait_db_connection(engine):
    for i in range(0, 20):
        try:
            engine.connect().scalar('SELECT 1')
            break
        except exc.OperationalError:
            sleep(1)
            print(f'connecting to DB..{i}')
    else:
        engine.connect().scalar('SELECT 1')


engine = create_engine(
    URL(
        drivername='postgresql+psycopg2',
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_DATABASE'),
        username=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD')
    )
)
_wait_db_connection(engine)
session = scoped_session(sessionmaker(bind=engine))
session_maker = sessionmaker(bind=engine)


def init_db():
    BaseModel.query = session.query_property()
    try:
        BaseModel.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        # TODO catch sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation)
        pass
