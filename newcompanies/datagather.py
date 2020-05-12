import datetime
import json
import operator
import os
import time
from inflection import underscore

import requests
from sqlalchemy import func

from crud import get_or_create, get_or_create_from_instance,\
                 get_company_extremes
from database import connect_to_db, DB
from models import Company, Address

# .\env\Scripts\activate

COMPANY_DATA_URL = 'http://data.companieshouse.gov.uk/doc/company/'
FORMAT = '.json'
TEST_COMPANY_NUMBER = 12586212


def get_company_data(company_number:int) -> dict:
    """Return a dict of official company data from Companies House
    based on the input company number.
    """
    
    r = requests.get(COMPANY_DATA_URL + str(company_number) + FORMAT)
    
    if r.text[0] == '<':
        return False
    
    data = json.loads(r.text)['primaryTopic']
    
    return data


def company_data_to_model(data: dict) -> Company:
    """Returns an instance of the Company class for the input data, where data 
    is the standard format from Companies House.
    """

    date = data['IncorporationDate'].split('/')
    
    dt = datetime.date(int(date[2]),int(date[1]),int(date[0]))
    
    company = Company(number=int(data['CompanyNumber']), 
                      name=data['CompanyName'], 
                      incorporated=dt)
    
    return company


def data_to_address_dict(data: dict) -> dict:
    """Returns an instance of the Address class for the input data, where data
    is the standard format from Companies House.
    """

    address_dict = {}

    for key,value in data['RegAddress'].items():
        address_dict[underscore(key)] = data['RegAddress'][key]
 
    # address_dict['occupier_id'] = int(data['CompanyNumber'])

    address = Address(**address_dict)

    return address_dict, address

def get_and_add_companies(start_point: int, session, asc: bool=True):
    """Given a company number as the starting point and choosing a direction, 
    add companies above/below the starting point to the database sequentially.
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
        address = data_to_address_dict(data)[1]
        print(company)
        print(address)
        instance = get_or_create(session, Company, number=company.number, 
                                 name=company.name, 
                                 incorporated=company.incorporated)
        instance.address = address
        session.add(instance)
        session.commit()
        # get_or_create(session, Address, **address)
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