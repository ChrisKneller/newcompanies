import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
from classes import Base, Company, Test
import decimal, datetime

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


def alchemyencoder(obj):
    """
    JSON encoder function for SQLAlchemy special classes.
    """

    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def get_or_create(session, model, **kwargs):
    """
    Check if an item exists inside the database, add it if it doesn't.
    """

    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_company_extremes(session):
    """
    Return a tuple of the lowest and the highest company number stored in the companies table, respectively.
    """

    query = session.query(
        db.func.max(Company.number).label("max"),
        db.func.min(Company.number).label("min"))
    res = query.one()
    return res.min, res.max


def get_company_by_date(session, query=None, **kwargs):
    """Return an ordered Company query object filtered by date.

    Args:
        session (sqlalchemy.orm.session.Session): A session connected to the database.
        **kwargs: year, month or day

    Returns:
        sqlalchemy.orm.query.Query: A query result filtered by the input kwargs.
    """    
    if not query:
        query = session.query(Company)
    for key, value in kwargs.items():
        query = query.filter(db.extract(key, Company.incorporated_on)==value)
    return query.order_by(Company.number)


def filter_query(query, **kwargs):
    for key,value in kwargs.items():
        query = query.filter_by(**{key:value})
    return query.order_by(Company.number)

if __name__ == "__main__":
    SESSION = connect_to_db(DB)