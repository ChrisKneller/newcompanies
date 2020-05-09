from sqlalchemy.orm import Session, Query
import sqlalchemy as db

from newcompanies import models, schemas


### HELPER FUNCTIONS ###


def get_or_create(session: Session, model, **kwargs):
    """
    Check if an item exists inside the database; add it if it doesn't.
    """

    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance


def get_company_extremes(session: Session):
    """
    Return a tuple of the lowest and the highest company number stored in the companies table, respectively.
    """

    query = session.query(
        db.func.max(models.Company.number).label("max"),
        db.func.min(models.Company.number).label("min"))
    res = query.one()
    return res.min, res.max


def filter_query(query: Query, **kwargs):
    """Filter an input query for the given kwargs.

    Args:
        query (Query): An existing query from the database.
        **kwargs: A column from the database.

    Returns:
        [type]: [description]
    """
    for key,value in kwargs.items():
        query = query.filter_by(**{key:value})
    return query


### COMPANY FUNCTIONS ###

    
def create_company(session: Session, company: schemas.CompanyCreate):
    """
    Create a company from the CompanyCreate schema. Call get_or_create so it isn't added if it's a duplicate.
    Return the company that was added or that already existed.
    """

    db_company = models.Company(number=company.number, name=company.name, incorporated=company.incorporated)
    return get_or_create(session, db_company)


def get_company_by_id(session: Session, number: int):
    return session.query(models.Company).filter(models.Company.number == number).first()


def get_company_by_date(session: Session, query: Query = None, **kwargs):
    """Return an ordered Company query object filtered by date.

    Args:
        session (Session): A session connected to the database.
        query (Query): An existing query from the database.
        **kwargs: year, month or day (int).

    Returns:
        sqlalchemy.orm.query.Query: A query result filtered by the input kwargs.
    """    
    if not query:
        query = session.query(models.Company)
    for key, value in kwargs.items():
        query = query.filter(db.extract(key, models.Company.incorporated)==value)
    return query.order_by(models.Company.number)