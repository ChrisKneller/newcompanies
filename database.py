import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
from classes import Base, Company, Test

DB = os.environ.get('NC_DB_URL')
USER = os.environ.get('NC_DB_USER')
PW = os.environ.get('NC_DB_PW')

def connect_to_db(database=DB):
    engine = db.create_engine(database, echo=True)
    connection = engine.connect()
    metadata = db.MetaData()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    