import sqlalchemy as db
import os
from classes import Base, Company, Test

DB = os.environ.get('NC_DB_URL')
USER = os.environ.get('NC_DB_USER')
PW = os.environ.get('NC_DB_PW')

def connect_to_db(database=DB):
    engine = db.create_engine(database, echo=True)
    connection = engine.connect()
    metadata = db.MetaData()
    return engine, metadata

def update_tables(engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    engine, metadata = connect_to_db()