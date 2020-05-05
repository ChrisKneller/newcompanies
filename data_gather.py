import requests
import json
import os
from database import connect_to_db, DB
from classes import Company
import datetime
import operator

# .\env\Scripts\activate

COMPANY_DATA_URL = 'http://data.companieshouse.gov.uk/doc/company/'
FORMAT = '.json'
TEST_COMPANY_NUMBER = 12586212

SESSION = connect_to_db(DB)

def get_company_data(company_number:int) -> dict:
    """
    Return a dict of official company data from Companies House
    based on the input company number.
    """
    r = requests.get(COMPANY_DATA_URL + str(company_number) + FORMAT)
    if r.text[0] == '<':
        return False
    data = json.loads(r.text)['primaryTopic']
    return data

def company_data_to_model(data):
    """
    Returns an instance of the Company class for the input data, where data is the standard format from Companies House.
    """
    date = data['IncorporationDate'].split('/')
    dt = datetime.date(int(date[2]),int(date[1]),int(date[0]))
    company = Company(number=int(data['CompanyNumber']), name=data['CompanyName'], incorporated_on=dt)
    return company

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

def get_and_add_companies(start_point: int, asc=True, session=SESSION):
    """
    Get company data for all companies after the input company.
    """
    company_number = start_point
    op = operator.add if asc else operator.sub
    while True:
        data = get_company_data(company_number)
        if not data:
            company_number = op(company_number,1)
            continue
        company = company_data_to_model(data)
        instance = get_or_create(session, Company, number=company.number, name=company.name, incorporated_on=company.incorporated_on)
        company_number = op(company_number,1)
    return instance
