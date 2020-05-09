import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
from newcompanies.models import Base, Company, Test
import decimal
import datetime

DB = os.environ.get('NC_DB_URL')
USER = os.environ.get('NC_DB_USER')
PW = os.environ.get('NC_DB_PW')


def connect_to_db(database=DB):
    """
    Connect to the given database and return a session.
    """

    engine = db.create_engine(database, echo=True)
    connection = engine.connect()
    metadata = db.MetaData()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    SESSION = connect_to_db(DB)