import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models._base import BaseModel


engine = create_engine(os.getenv("DATABASE_URL"))
session = scoped_session(sessionmaker(bind=engine))


def init_db():
    BaseModel.query = session.query_property()
    # BaseModel.metadata.create_all(bind=engine)
