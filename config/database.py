import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
session = sessionmaker(bind=engine)()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()