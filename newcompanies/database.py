import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import decimal
import datetime


DB = os.environ.get('NC_DB_URL')
USER = os.environ.get('NC_DB_USER')
PW = os.environ.get('NC_DB_PW')

engine = db.create_engine(DB)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()

def connect_to_db(database=DB):
    """
    Connect to the given database and return a session.
    """

    engine = db.create_engine(database, echo=True)
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# if __name__ == "__main__":
#     SESSION = connect_to_db(DB)