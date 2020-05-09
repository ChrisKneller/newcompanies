from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from .datagather import get_company_data
from .database import connect_to_db, DB, get_company_by_date, filter_query
from .models import Company
from .functions import alchemyencoder, to_json
import json
import datetime

# uvicorn main:app --reload
# env\Scripts\activate.bat

app = FastAPI()

SESSION = connect_to_db(DB)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/company/{company_id}")
async def read_company(company_id: int):
    company = get_company_data(company_id)
    return company if company else None


@app.get("/companies")
def get_companies(year=False, month=False, day=False, number=False, name=False):
    arguments = locals()
    if not any(arguments.values()):
        return None
    query = SESSION.query(Company).order_by(Company.number)
    for key, value in arguments.items():
        if not value:
            continue
        if key == 'year' or key == 'month' or key == 'day':
            query = get_company_by_date(SESSION, query, **{key:value})
        else:
            query = filter_query(query, **{key:value})
    return {"companies": [i.as_json() for i in query]} if query else {None}


@app.get("/testrequest")
def test_request():
    query = SESSION.query(Company).order_by(Company.number).filter_by(name="PAARTI LTD")
    # return json.dumps({"company": i.to_dict() for i in query}, default=alchemyencoder)
    return {"company": [i for i in query]}
    # return Response(to_json(query[0])})


@app.get("/incorporated/today")
def get_companies_today():
    today = datetime.datetime.now()
    return get_companies_by_day(today.year, today.month, today.day)


# @app.gt("/incorporated")
# def get_companies(**kwargs):



@app.get("/incorporated/{year}/{month}/{day}")
def get_companies_by_day(year: int, month: int, day: int):
    query = get_company_by_date(SESSION, year=year, month=month, day=day)
    # query = SESSION.query(Company).filter_by(incorporated_on=f"{year}-{month}-{day}").all()
    return {"companies": [i.as_json() for i in query]}


@app.get("/incorporated/{year}/{month}")
def get_companies_by_month(year: int, month: int):
    query = get_company_by_date(SESSION, year=year, month=month)
    return {"companies": [i.as_json() for i in query]}


@app.get("/incorporated/{year}")
def get_companies_by_year(year: int):
    query = get_company_by_date(SESSION, year=year)
    return {"companies": [i.as_json() for i in query]}