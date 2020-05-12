from sqlalchemy.orm import Session, Query
import sqlalchemy as db
from sqlalchemy import extract, func

from newcompanies import models, schemas

import datetime


### HELPER FUNCTIONS ###


def get_or_create(session: Session, model, **kwargs):
    """Check if an item exists inside the database; add it if it doesn't.
    """
<<<<<<< HEAD
    print(kwargs)
=======

>>>>>>> 0e9147aac53922f29ddd4021f53e77e0df9659ee
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance


def get_or_create_from_instance(session, model, instance):
    """Check if a created instance exists inside the database; add it if it
    doesn't.
    """

    arguments = instance.__dict__
    print(arguments)
    arguments.pop("_sa_instance_state")

    exist_instance = session.query(model).filter_by(**arguments).one_or_none()
    if exist_instance:
        return exist_instance
    else:
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance


def get_company_extremes(session: Session):
    """Return a tuple of the lowest and the highest company number stored in 
    the companies table, respectively.
    """

    query = session.query(
        func.max(models.Company.number).label("max"),
        func.min(models.Company.number).label("min"))
    res = query.one()
    return res.min, res.max


def filter_query(query: Query, **kwargs):
    """Filter an input query for the given kwargs.

    Args:
        query (Query): An existing query from the database.
        **kwargs: A column from the database.

    Returns:
        query (Query): The filtered query.
    """
    for key,value in kwargs.items():
        query = query.filter_by(**{key:value})
    return query


### COMPANY FUNCTIONS ###

    
def create_company(session: Session, company: schemas.CompanyCreate):
    """Create a company from the CompanyCreate schema. Call get_or_create so it
    isn't added if it's a duplicate.

    Return the company that was added or that already existed.
    """

    db_company = models.Company(number=company.number, name=company.name, 
                                incorporated=company.incorporated)
    
    return get_or_create(session, db_company)


def get_cos(session: Session, skip: int = 0, limit: int = 20000):
    return session.query(models.Company).offset(skip).limit(limit).all()


def get_company_by_date(session: Session, query: Query = None, **kwargs):
    """Return an ordered Company query object filtered by date.

    Args:
        session (Session): A session connected to the database.
        **kwargs: year, month or day (int).

    Returns:
        query (Query): A query result filtered by the input kwargs.
    """    
    if not query:
        query = session.query(models.Company)
    for key, value in kwargs.items():
        query = query.filter(extract(key, models.Company.incorporated)==value)
    return query



def get_companies(session: Session, skip: int = 0, limit: int = None, 
                  year: int = None, month: int = None, day: int = None, 
                  **kwargs):
    arguments = locals()[3:]
    if not any(arguments.values()):
        return None
    query = session.query(models.Company)
    for key, value in arguments.items():
        if not value:
            continue
        if key == 'year' or key == 'month' or key == 'day':
            query = get_company_by_date(session, query, **{key:value})
        else:
            query = filter_query(query, **{key:value})
    print(query)
    return query.all()



def get_company_by_id(session: Session, number: int):
    return (session.query(models.Company)
            .filter(models.Company.number == number).first())
