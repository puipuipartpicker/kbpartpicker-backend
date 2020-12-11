
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgres+psycopg2://vi:password@localhost:5432/kbpartpicker')
session = sessionmaker(bind=engine)()