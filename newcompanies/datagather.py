import requests
import json
import os
from .database import connect_to_db, DB, get_or_create, get_company_extremes
from .models import Company
import datetime
import operator
from sqlalchemy import func
import time

# .\env\Scripts\activate

COMPANY_DATA_URL = 'http://data.companieshouse.gov.uk/doc/company/'
FORMAT = '.json'
TEST_COMPANY_NUMBER = 12586212

# SESSION = connect_to_db(DB)


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
    company = Company(number=int(data['CompanyNumber']), name=data['CompanyName'], incorporated=dt)
    return company


def get_and_add_companies(start_point: int, session, asc: bool=True):
    """
    Given a company number as the starting point and choosing a direction, add companies above or below
    the starting point to the database sequentially.
    """

    company_number = start_point
    op = operator.add if asc else operator.sub
    tries = 0
    trylim = 10
    while tries < 150:
        data = get_company_data(company_number)
        if not data:
            if asc == False or tries > trylim:
                company_number = op(company_number,1)
                trylim += 10
            else:
                tries += 1
                time.sleep(120)
            continue
        company = company_data_to_model(data)
        instance = get_or_create(session, Company, number=company.number, name=company.name, incorporated=company.incorporated)
        company_number = op(company_number,1)
    return instance

if __name__ == "__main__":
    SESSION = connect_to_db(DB)
    x = input("Up or down? ")
    minco, maxco = get_company_extremes(SESSION)
    if x == 'up':
        get_and_add_companies(maxco, SESSION)
    elif x == 'down':
        get_and_add_companies(minco, SESSION, asc=False)
    else:
        pass